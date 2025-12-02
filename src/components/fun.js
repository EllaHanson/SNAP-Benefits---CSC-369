import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

const data = await d3.csv("./data/snap_clean.csv", i => ({
  date: d3.timeParse("%Y-%m-%d")(i.date),
  state: i.state,
  true_person: +i.true_person
}));

// group by state and filter bad rows
const state_data = d3.group(
    data.filter(i => i.true_person && i.date),
    i => i.state
);

const margin = {top: 20, right: 100,  bottom: 30, left: 60};
const width = 900;
const height = 500;

const x = d3.scaleTime()
    .domain(d3.extent(data, i => i.date))
    .range([margin.left, width - margin.right]);

const y = d3.scaleLinear()
    .domain([0, d3.max(data, i => i.true_person)]).nice()
    .range([height - margin.bottom, margin.top]);

const color = d3.scaleOrdinal()
    .domain([...dataByState.keys()])
    .range(d3.schemeCategory10);

const line = d3.line()
    .x(i => x(date))
    .y(i => y(i.true_person));

const svg = d3.create("svg")
    .attr("viewBox", [0, 0, width, height]);

svg.append("g")
    .attr("transform", `translate(0, ${height - margin.bottom})`)
    .call(d3.axisBottom(x));

svg.append("g")
    .attr("transform", `translate(${margin.left}, 0)`)
    .call(d3.axisLeft(y));

for (const [state,  values] of state_data) {
    svg.append("path")
        .datum(sorted)
        .attr("fill", "none")
        .attr("stroke", color(state))
        .attr("stroke-width", 1.6)
        .attr("d", line);
}

return svg.node();