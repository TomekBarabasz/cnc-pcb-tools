module Bezier

export Point, Curve, PointF32, CurveF32, read_svg_paths, parse_svg_path

import Base: +,-

struct Point{T<:AbstractFloat}
    x::Float32
    y::Float32
end
+(p1::Point{T}, p2::Point{T}) where T = Point{T}(p1.x + p2.x, p1.y + p2.y)

struct Curve{T<:AbstractFloat} 
    start_pt::Point{T}
    c1::Point{T}
    c2::Point{T}
    end_pt::Point{T}  # 'end' is a keyword in Julia
end

const PointF32 = Point{Float32}
const CurveF32 = Curve{Float32}

end #module
