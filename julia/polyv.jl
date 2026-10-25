import DelaunayTriangulation as DT

include("CncTools/src/CncTools.jl")
using .CncTools: Point, make_test_shape

function calc_medial_axis(points::Vector{Point{T}}) where T<:AbstractFloat
    tri = triangulate([(p.x,p.y) for p in points])
    vor = voronoi(tri)

    

    voronoi_points
end

function voronoi_pocketing(outer_shape::Vector{Point{T}}, tool_dia, stepover, 
        finish::Bool = true, include_arcs::Bool = true; 
        islands::Union{Nothing,Vector{Point{T}}}) where T<:AbstractFloat

    tri = triangulate([ (p.x,p.y) for p in outer_shape ])
    vor = voronoi(tri)

    # Collect Voronoi vertices
    voronoi_points = Vector{PointF32}()
    for cell in vor.cells
        for v_idx in cell.vertices
            v = vor.vertices[v_idx]
            push!(voronoi_points, PointF32(v.x, v.y))
        end
    end

    # Offset Voronoi edges to create tool paths
    tool_paths = Vector{Vector{PointF32}}()
    for edge in vor.edges
        p1 = vor.vertices[edge.start_vertex]
        p2 = vor.vertices[edge.end_vertex]
        line_points = [PointF32(p1.x, p1.y), PointF32(p2.x, p2.y)]
        offset_path = Poly.offset_polyline(line_points, tool_dia, max_error)
        push!(tool_paths, offset_path)
    end

    tool_paths
end
