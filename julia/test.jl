using ArgParse
using GLMakie

include("CncTools/src/CncTools.jl")
using .CncTools

function parse_commandline()
    s = ArgParseSettings()
    @add_arg_table s begin
        "test_name"
            help = "test name"
            required = true
    end
    args = parse_args(s)
    (; (Symbol(k) => v for (k, v) in args)...)
end

function plot_polylines(polys)
    fig = Figure()
    ax = Axis(fig[1, 1], aspect = DataAspect())
    for (poly,color) in zip(polys,[:red,:blue,:green])
        xs, ys = [p.x for p in poly], [p.y for p in poly]
        lines!(ax, xs, ys, color = color)
        scatter!(ax, xs, ys, markersize = 5, color = color)
    end
    wait(display(fig))
end

args = parse_commandline()
test_name = args[:test_name]
test_shapes = Utils.make_test_shapes(Float32)

pts = test_shapes[test_name]

tool_dia, max_error = 0.1f0, 0.01f0
cnc_pts = offset_polyline(pts, tool_dia, max_error)
plot_polylines((cnc_pts, pts))
