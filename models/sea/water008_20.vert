//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslv
//program vshader
//semantic vshader.k_fogexpdensity
//semantic vshader.k_map
//semantic vshader.k_alphamap
//semantic vshader.trans_view_to_world
//semantic vshader.trans_model_to_view
//semantic vshader.trans_model_to_apiclip
//var float4 k_fogexpdensity :  : _k_fogexpdensity1 : 10 : 1
//\--replaced with fogexpdensity
//var float4 k_map :  : _k_map1 : 11 : 1
//\--replaced with map
//var float4 k_alphamap :  : _k_alphamap1 : 12 : 1
//\--replaced with alphamap
//var float4x4 trans_view_to_world :  : _trans_view_to_world1[0], 4 : 13 : 1
//\--replaced with trans_view_to_world
//var float4x4 trans_model_to_view :  : _trans_model_to_view1[0], 4 : 14 : 1
//\--replaced with trans_model_to_view
//var float4x4 trans_model_to_apiclip :  : _trans_model_to_apiclip1[0], 4 : 15 : 1
//\--replaced with trans_model_to_apiclip
//var float3 vtx_position : $vin.POSITION : ATTR0 : 0 : 1
//\--replaced with p3d_Vertex
//var float3 vtx_normal : $vin.NORMAL : ATTR2 : 1 : 1
//\--replaced with normal
//var float2 vtx_texcoord0 : $vin.TEXCOORD0 : ATTR8 : 2 : 1
//\--replaced with p3d_MultiTexCoord0
//var float4 l_position : $vout.POSITION : HPOS : 3 : 1
//var float2 l_texcoord0 : $vout.TEXCOORD0 : TEX0 : 4 : 1
//var float4 l_texcoord1 : $vout.TEXCOORD1 : TEX1 : 5 : 1
//var float3 l_normal : $vout.TEXCOORD2 : TEX2 : 6 : 1
//var float3 l_surface_pos : $vout.TEXCOORD3 : TEX3 : 7 : 1
//var float3 l_interpolate : $vout.TEXCOORD4 : TEX4 : 8 : 1
//var float2 l_alpha_uv : $vout.TEXCOORD5 : TEX5 : 9 : 1

#version 120

vec4 _l_position1;
vec3 _l_interpolate1;
vec4 _l_texcoord11;
vec3 _l_surface_pos1;
vec2 _l_texcoord01;
vec2 _l_alpha_uv1;
vec3 _l_normal1;
uniform vec4 fogexpdensity;
uniform vec4 map;
uniform vec4 alphamap;
uniform vec4 trans_view_to_world[4];
uniform vec4 trans_model_to_view[4];
uniform vec4 trans_model_to_apiclip[4];
vec4 _r0010;
vec4 _r0020;
vec4 _r0030;
float _TMP39;
float _x0040;
vec4 _r0044;

 // main procedure, the original name was vshader
void main()
{

    vec4 _vertex;

    _vertex.xyz = gl_Vertex.xyz;
    _vertex.w = 1.00000000E+00;
    _r0010.x = dot(trans_model_to_apiclip[0], _vertex);
    _r0010.y = dot(trans_model_to_apiclip[1], _vertex);
    _r0010.z = dot(trans_model_to_apiclip[2], _vertex);
    _r0010.w = dot(trans_model_to_apiclip[3], _vertex);
    _l_normal1 = gl_Normal;
    _l_surface_pos1 = gl_Vertex.xyz;
    _l_texcoord01 = gl_MultiTexCoord0.xy;
    _r0020.x = dot(trans_model_to_view[0], _vertex);
    _r0020.y = dot(trans_model_to_view[1], _vertex);
    _r0020.z = dot(trans_model_to_view[2], _vertex);
    _r0020.w = dot(trans_model_to_view[3], _vertex);
    _r0030.x = dot(trans_view_to_world[0], _r0020);
    _r0030.y = dot(trans_view_to_world[1], _r0020);
    _l_interpolate1.xy = (_r0030.xy - map.xy)*map.zw;
    _l_alpha_uv1.xy = (_r0030.xy - alphamap.xy)*alphamap.zw;
    _x0040 = -(fogexpdensity.x*_r0020.y);
    _TMP39 = pow(2.71828198E+00, _x0040);
    _l_interpolate1.z = 1.00000000E+00 - _TMP39;
    _r0044.x = dot(vec4( 5.00000000E-01, 0.00000000E+00, 0.00000000E+00, 5.00000000E-01), _r0010);
    _r0044.y = dot(vec4( 0.00000000E+00, 5.00000000E-01, 0.00000000E+00, 5.00000000E-01), _r0010);
    _r0044.z = dot(vec4( 0.00000000E+00, 0.00000000E+00, 5.00000000E-01, 5.00000000E-01), _r0010);
    _r0044.w = dot(vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00), _r0010);
    _l_texcoord11 = _r0044;
    _l_position1 = _r0010;
    gl_TexCoord[2].xyz = gl_Normal;
    gl_TexCoord[5].xy = _l_alpha_uv1;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_TexCoord[3].xyz = gl_Vertex.xyz;
    gl_TexCoord[1] = _r0044;
    gl_TexCoord[4].xyz = _l_interpolate1;
    gl_Position = _r0010;
} // main end
