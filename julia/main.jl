using ArgParse

include("svg.jl")
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


args = parse_commandline()
paths = read_svg_paths(args.input_filename)
path11 = paths["path11"]

curves = parse_svg_path(Float32, path11)
