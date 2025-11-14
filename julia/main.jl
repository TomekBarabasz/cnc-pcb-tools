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
        "--simple"
            action = :store_true
        "--tool_dia"
            arg_type = Float32
            default = 0.2
        "--max_error"
            arg_type = Float32
            default = 0.01
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

function make_test_shape(T::Type{<:Number}, name)
    Pt = Point{T}
    if name == "square"
        ret = [Pt(0,0),Pt(0,1),Pt(1,1),Pt(1,0), Pt(0,0)]
    elseif name == "square-2"
        ret = [Pt(0,0),Pt(0.5,0),Pt(1,0),Pt(1,-0.5), Pt(1,-1), Pt(0.5,-1),Pt(0,-1),Pt(0,-0.5),Pt(0,0)]
    elseif name == "star"
        ret = [Pt(0,0),Pt(3,1),Pt(4,4),Pt(5,1),Pt(8,0),Pt(5,-1),Pt(4,-4),Pt(3,-1),Pt(0,0)]
    elseif name == "butterfly"
        ret = [Pt(0,0),Pt(0,3),Pt(2,4),Pt(0,5),Pt(0,8),Pt(3,8),Pt(4,6),Pt(5,8),Pt(8,8),
               Pt(8,5),Pt(6,4),Pt(8,3),Pt(8,0),Pt(5,0),Pt(4,2),Pt(3,0),Pt(0,0)]
    elseif name == "hex"
        ret = [Pt(0,1),Pt(0,3),Pt(1,4),Pt(3,4),Pt(4,3),Pt(4,1),Pt(3,0),Pt(1,0),Pt(0,1)]
    else
        ret = nothing
    end
    ret
end

function make_test_shapes(T::Type{<:Number})
    Dict{String, Vector{Bezier.Point{T}}}(n => make_test_shape(T,n) for n in ["square", "star", "butterfly", "hex"])
end

args = parse_commandline()
basic_point_curve_tests()

paths = read_svg_paths(args.input_filename)
path11 = paths["path11"]
curves = parse_svg_path(Float32, path11)
tool_dia = args.tool_dia
max_error = args.max_error
pts = remove_duplicate_points(flattenr(curves,max_error),max_error)
cnc_pts = make_cnc_path(pts, tool_dia, max_error)

plot_polylines((cnc_pts, pts))

#test_offset_curve(args)



