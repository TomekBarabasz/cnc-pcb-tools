using ArgParse
using GLMakie

include("Bezier.jl")
include("SVG.jl")
include("Poly.jl")
using .Bezier
using .SVG
using .Poly

function parse_commandline()
    s = ArgParseSettings()
    @add_arg_table s begin
        "input_filename"
            help = "Input filnemae"
            required = true
    end
    args = parse_args(s)
    (; (Symbol(k) => v for (k, v) in args)...)
end

function basic_point_curve_tests()
    p1 = PointF32(1,1)
    p2 = PointF32(2,2)
    p3 = p1+p2
    p4 = p1 * 3.f0
    p5 = p4 / 2.f0

    p12 = midpoint(p1,p2)

    c = CurveF32(p1,p2,p3,p4)
    c1,c2 = subdivide(c)
    pl = flatten(c,0.01)
end

function plot_polyline(points)
    xs, ys = [p.x for p in points], [p.y for p in points]
    fig = Figure()
    ax = Axis(fig[1, 1], aspect = DataAspect())
    lines!(ax, xs, ys)
    scatter!(ax, xs, ys, markersize = 5)
    wait(display(fig))
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

basic_point_curve_tests()

paths = read_svg_paths(args.input_filename)
path11 = paths["path11"]
curves = parse_svg_path(Float32, path11)
pts = flatten(curves,0.01)

#pts_i = offset_polyline_simple(pts, -3)
#pts_o = offset_polyline_simple(pts, 3)

pts_i = offset_polyline(pts, -3)
pts_o = offset_polyline(pts, 3)

plot_polylines((pts_i, pts, pts_o))

