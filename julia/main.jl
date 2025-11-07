using ArgParse

include("Bezier.jl")
include("SVG.jl")
using .Bezier: PointF32, midpoint, CurveF32, subdivide, flatten
using .SVG

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

args = parse_commandline()

basic_point_curve_tests()

paths = read_svg_paths(args.input_filename)
path11 = paths["path11"]
curves = parse_svg_path(Float32, path11)
println("nbr of curves in path11 : $(length(curves))")
println("c[begin] = $(curves[begin])")
pts = flatten(curves,0.01)
println("nbr of points after flatten : $(length(pts))")
l1 = flatten(curves[begin],0.1)
println("l1=$(l1)")
