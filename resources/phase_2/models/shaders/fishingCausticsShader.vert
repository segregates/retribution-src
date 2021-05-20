//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslv
//program vshader
//semantic vshader.mat_modelproj
//semantic vshader.mat_modelview
//semantic vshader.inv_modelview
//semantic vshader.inv_modelproj
//semantic vshader.trans_model_to_world
//semantic vshader.trans_world_to_model
//semantic vshader.k_sunWorldLocation
//var float4x4 mat_modelproj :  : _mat_modelproj1[0], 4 : 3 : 1
//\--replaced with mat_modelproj
//var float4x4 inv_modelview :  : _inv_modelview1[0], 4 : 5 : 1
//\--replaced with inv_modelview
//var float4x4 trans_model_to_world :  : _trans_model_to_world1[0], 4 : 7 : 1
//\--replaced with trans_model_to_world
//var float4x4 trans_world_to_model :  : _trans_world_to_model1[0], 4 : 8 : 1
//\--replaced with trans_world_to_model
//var float4 k_sunWorldLocation :  : _k_sunWorldLocation1 : 9 : 1
//\--replaced with sunWorldLocation
//var float4 vtx_position : $vin.POSITION : ATTR0 : 0 : 1
//\--replaced with p3d_Vertex
//var float2 vtx_texcoord0 : $vin.TEXCOORD0 : ATTR8 : 1 : 1
//\--replaced with p3d_MultiTexCoord0
//var float3 vtx_normal : $vin.NORMAL : ATTR2 : 2 : 1
//\--replaced with normal
//var float4 l_position : $vout.POSITION : HPOS : 10 : 1
//var float2 l_texcoord0 : $vout.TEXCOORD0 : TEX0 : 11 : 1
//var float3 l_halfVec : $vout.TEXCOORD1 : TEX1 : 12 : 1
//var float4 l_eyevec : $vout.TEXCOORD2 : TEX2 : 13 : 1
//var float3 l_normal : $vout.TEXCOORD3 : TEX3 : 14 : 1
//var float4 l_worldPos : $vout.TEXCOORD4 : TEX4 : 15 : 1
//var float4 l_lightVec0 : $vout._l_lightVec01 : _l_lightVec01 : 16 : 1

#version 120

vec4 _l_position1;
vec4 _l_worldPos1;
vec3 _l_halfVec1;
vec3 _l_normal1;
vec2 _l_texcoord01;
vec4 _l_eyevec1;
varying vec4 _l_lightVec01;
float _TMP1;
float _TMP0;
uniform vec4 mat_modelproj[4];
uniform vec4 inv_modelview[4];
uniform vec4 trans_model_to_world[4];
uniform vec4 trans_world_to_model[4];
uniform vec4 sunWorldLocation;
vec4 _r0020;
vec4 _r0030;
vec4 _r0046;
vec4 _r0062;
vec3 _v0072;
vec3 _v0080;

 // main procedure, the original name was vshader
void main()
{


    _l_texcoord01 = gl_MultiTexCoord0.xy;
    _r0020.x = dot(mat_modelproj[0], gl_Vertex);
    _r0020.y = dot(mat_modelproj[1], gl_Vertex);
    _r0020.z = dot(mat_modelproj[2], gl_Vertex);
    _r0020.w = dot(mat_modelproj[3], gl_Vertex);
    _l_position1 = _r0020;
    _r0030.x = dot(trans_model_to_world[0], gl_Vertex);
    _r0030.y = dot(trans_model_to_world[1], gl_Vertex);
    _r0030.z = dot(trans_model_to_world[2], gl_Vertex);
    _r0030.w = dot(trans_model_to_world[3], gl_Vertex);
    _l_worldPos1 = _r0030;
    _TMP0 = dot(gl_Normal, gl_Normal);
    _TMP1 = inversesqrt(_TMP0);
    _l_normal1.xyz = _TMP1*gl_Normal;
    _r0046.x = dot(trans_world_to_model[0], sunWorldLocation);
    _r0046.y = dot(trans_world_to_model[1], sunWorldLocation);
    _r0046.z = dot(trans_world_to_model[2], sunWorldLocation);
    _TMP0 = dot(_r0046.xyz, _r0046.xyz);
    _TMP1 = inversesqrt(_TMP0);
    _l_lightVec01.xyz = _TMP1*_r0046.xyz;
    _r0062.x = dot(inv_modelview[0], vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00));
    _r0062.y = dot(inv_modelview[1], vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00));
    _r0062.z = dot(inv_modelview[2], vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00));
    _r0062.w = dot(inv_modelview[3], vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00));
    _v0072 = (_r0062 - gl_Vertex).xyz;
    _TMP0 = dot(_v0072, _v0072);
    _TMP1 = inversesqrt(_TMP0);
    _l_eyevec1.xyz = _TMP1*_v0072;
    _l_eyevec1.w = length(_r0062.xyz);
    _v0080 = _l_eyevec1.xyz + _l_lightVec01.xyz;
    _TMP0 = dot(_v0080, _v0080);
    _TMP1 = inversesqrt(_TMP0);
    _l_halfVec1 = _TMP1*_v0080;
    _l_eyevec1 = _l_eyevec1*5.00000000E-01;
    _l_eyevec1 = _l_eyevec1 + 5.00000000E-01;
    gl_TexCoord[2] = _l_eyevec1;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_TexCoord[3].xyz = _l_normal1;
    gl_TexCoord[1].xyz = _l_halfVec1;
    gl_TexCoord[4] = _r0030;
    gl_Position = _r0020;
} // main end
