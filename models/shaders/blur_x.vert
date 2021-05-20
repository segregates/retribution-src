//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslv
//program vshader
//semantic vshader.mat_modelproj
//var float4x4 mat_modelproj :  : _mat_modelproj1[0], 4 : 4 : 1
//\--replaced with mat_modelproj
//var float4 vtx_position : $vin.POSITION : ATTR0 : 0 : 1
//\--replaced with p3d_Vertex
//var float2 vtx_texcoord0 : $vin.TEXCOORD0 : ATTR8 : 1 : 1
//\--replaced with p3d_MultiTexCoord0
//var float4 l_position : $vout.POSITION : HPOS : 2 : 1
//var float2 l_texcoord0 : $vout.TEXCOORD0 : TEX0 : 3 : 1

#version 120

vec4 _l_position1;
vec2 _l_texcoord01;
uniform vec4 mat_modelproj[4];
vec4 _r0002;

 // main procedure, the original name was vshader
void main()
{


    _r0002.x = dot(mat_modelproj[0], gl_Vertex);
    _r0002.y = dot(mat_modelproj[1], gl_Vertex);
    _r0002.z = dot(mat_modelproj[2], gl_Vertex);
    _r0002.w = dot(mat_modelproj[3], gl_Vertex);
    _l_position1 = _r0002;
    _l_texcoord01 = gl_MultiTexCoord0.xy;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_Position = _r0002;
} // main end
