---
toc: false
---

```js
import * as d3 from "npm:d3@7";
```

```js

// grabing csv file from data directory
const raw_data = await FileAttachment("data/snap_clean.csv").csv();

const data = raw_data.map(i => ({
  date: d3.timeParse("%Y-%m-%d")(i.date),
  state: i.state,
  true_person: +i.true_person
})).filter(i => i.date && i.state && !isNaN(i.true_person));

// get years in SNAP data
const years = Array.from(
    // make set by grabing year from date for every row
    new Set(data.map(i => i.date.getFullYear()))
).sort(d3.ascending)

// group by state
const state_data = d3.group(
    data,
    i => i.state
);

const margin = {top: 20, right: 100,  bottom: 30, left: 60};
const width = 900;
const height = 450;

// x-axis: timescale over the dates in the data
const x = d3.scaleTime()
    .domain(d3.extent(data, i => i.date))
    .range([margin.left, width - margin.right]);

// y-axis: linear scale from 0 to max benefits (then made pretty)
const y = d3.scaleLinear()
    .domain([0, d3.max(data, i => i.true_person)]).nice()
    .range([height - margin.bottom, margin.top]);

// make every state line a diff color
const color = d3.scaleOrdinal()
    .domain([...state_data.keys()])
    .range(d3.schemeCategory10);

// set x and y axis to date and benefits data
const line = d3.line()
    .x(i => x(i.date))
    .y(i => y(i.true_person));

// area holding both dropdown and chart
const container = document.createElement("div");

// label above start selection
const start_label = document.createElement("label");
start_label.textContent = "Start year";
// start year selection dropdown
const start_select = document.createElement("select");
start_label.appendChild(start_select);
container.appendChild(start_label);

// label above end selection
const end_label = document.createElement("label");
end_label.textContent = "End year";
// end year selection dropdown
const end_select = document.createElement("select");
end_label.appendChild(end_select);
container.appendChild(end_label);

//hovering showsstate name
const hover_label = document.createElement("div");
hover_label.textContent = "State: ...";
container.appendChild(hover_label);

// Add options to selectors
for (const year of years) {
    const opt1 = document.createElement("option");
    opt1.value = String(year);
    opt1.textContent = String(year);
    start_select.appendChild(opt1);

    const opt2 = document.createElement("option");
    opt2.value = String(year);
    opt2.textContent = String(year);
    end_select.appendChild(opt2);
}

// set orig start and end years
start_select.value = String(years[0]);
end_select.value = String(years[years.length - 1]);

const paths = new Map();

const svg = d3.create("svg")
    .attr("viewBox", [0, 0, width, height]);

const x_axis = svg.append("g")
    .attr("transform", `translate(0, ${height - margin.bottom})`)
    .call(d3.axisBottom(x));

const y_axis = svg.append("g")
    .attr("transform", `translate(${margin.left}, 0)`)
    .call(d3.axisLeft(y));

for (const [state,  values] of state_data) {
    const sorted_state_data = values.slice().sort((a,b) => a.date - b.date);

    const path = svg.append("path")
        .attr("fill", "none")
        .attr("stroke", color(state))
        .attr("stroke-width", 1.6);

    path.on("mouseenter", () => {
        path.attr("stroke-width", 3)
            .attr("opacity", 1);

        for (const [curr_state, {path: curr_path}] of paths) {
            if (curr_state !== state) {
                curr_path.attr("opacity", 0.2);
                curr_path.attr("stroke", "#888");
            }
        }

        hover_label.textContent = `State: ${state}`;
    });

    path.on("mouseleave", () => {
        for (const [curr_state, {path: curr_path}] of paths) {
            curr_path.attr("stroke-width", 1.6)
                .attr("opacity", 1)
                .attr("stroke", color(curr_state));
        }
        
        hover_label.textContent = "State: ...";
    });
    
    paths.set(state, { path, values: sorted_state_data});
}

function update() {
    // convert to nums
    const start_year = +start_select.value;
    const end_year = +end_select.value;

    const filtered_all = data.filter(i => {
        const year = i.date.getFullYear();
        return year >= start_year && year <= end_year;
    });

    if (!filtered_all.length) return;

    // redo scales
    x.domain(d3.extent(filtered_all, i => i.date));
    y.domain([0, d3.max(filtered_all, i => i.true_person)]).nice();

    x_axis.call(d3.axisBottom(x));
    y_axis.call(d3.axisLeft(y));

    for (const [state, {path, values}] of paths) {
        // only include years in selection
        const selected = values.filter(i => {
            const year = i.date.getFullYear();
            return (year >= start_year && year <= end_year);
        });
        if (selected.length) {
            path.attr("d", line(selected));
        }
        else {
            path.attr("d", null);
        }
    }

}

start_select.addEventListener("change", update);
end_select.addEventListener("change", update);

update();

container.appendChild(svg.node());
display(container);

```