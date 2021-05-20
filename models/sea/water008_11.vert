//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslv
//program vshader
//semantic vshader.k_lightposition
//semantic vshader.k_ambientcolor
//semantic vshader.k_diffusecolor
//semantic vshader.k_lightparameters
//semantic vshader.k_watercolor
//semantic vshader.k_fogexpdensity
//semantic vshader.k_map
//semantic vshader.k_alphamap
//semantic vshader.trans_view_to_world
//semantic vshader.trans_model_to_view
//semantic vshader.trans_model_to_apiclip
//var float4 k_lightposition :  : _k_lightposition1 : 9 : 1
//\--replaced with lightposition
//var float4 k_ambientcolor :  : _k_ambientcolor1 : 10 : 1
//\--replaced with ambientcolor
//var float4 k_diffusecolor :  : _k_diffusecolor1 : 11 : 1
//\--replaced with diffusecolor
//var float4 k_lightparameters :  : _k_lightparameters1 : 12 : 1
//\--replaced with lightparameters
//var float4 k_fogexpdensity :  : _k_fogexpdensity1 : 14 : 1
//\--replaced with fogexpdensity
//var float4 k_map :  : _k_map1 : 15 : 1
//\--replaced with map
//var float4 k_alphamap :  : _k_alphamap1 : 16 : 1
//\--replaced with alphamap
//var float4x4 trans_view_to_world :  : _trans_view_to_world1[0], 4 : 17 : 1
//\--replaced with trans_view_to_world
//var float4x4 trans_model_to_view :  : _trans_model_to_view1[0], 4 : 18 : 1
//\--replaced with trans_model_to_view
//var float4x4 trans_model_to_apiclip :  : _trans_model_to_apiclip1[0], 4 : 19 : 1
//\--replaced with trans_model_to_apiclip
//var float3 vtx_position : $vin.POSITION : ATTR0 : 0 : 1
//\--replaced with p3d_Vertex
//var float3 vtx_normal : $vin.NORMAL : ATTR2 : 1 : 1
//\--replaced with normal
//var float2 vtx_texcoord0 : $vin.TEXCOORD0 : ATTR8 : 2 : 1
//\--replaced with p3d_MultiTexCoord0
//var float4 l_position : $vout.POSITION : HPOS : 3 : 1
//var float2 l_texcoord0 : $vout.TEXCOORD0 : TEX0 : 4 : 1
//var float2 l_texcoord1 : $vout.TEXCOORD1 : TEX1 : 5 : 1
//var float2 l_interpolate : $vout.TEXCOORD2 : TEX2 : 6 : 1
//var float2 l_alpha_uv : $vout.TEXCOORD3 : TEX3 : 7 : 1
//var float4 l_color : $vout.COLOR0 : COL0 : 8 : 1

#version 120

vec4 _l_color1;
vec4 _l_position1;
vec2 _l_texcoord11;
vec2 _l_alpha_uv1;
vec2 _l_texcoord01;
vec2 _l_interpolate1;
float _TMP3;
float _TMP2;
uniform vec4 lightposition;
uniform vec4 ambientcolor;
uniform vec4 diffusecolor;
uniform vec4 lightparameters;
uniform vec4 fogexpdensity;
uniform vec4 map;
uniform vec4 alphamap;
uniform vec4 trans_view_to_world[4];
uniform vec4 trans_model_to_view[4];
uniform vec4 trans_model_to_apiclip[4];
vec4 _r0017;
vec4 _r0027;
vec4 _r0037;
float _TMP46;
float _x0047;
vec4 _r0051;
vec3 _v0061;
vec3 _v0067;

 // main procedure, the original name was vshader
void main()
{

    vec4 _vertex;
    float _diffuse;
    vec3 _light_direction;
    vec3 _opposite_light_direction;

    _vertex.xyz = gl_Vertex.xyz;
    _vertex.w = 1.00000000E+00;
    _r0017.x = dot(trans_model_to_apiclip[0], _vertex);
    _r0017.y = dot(trans_model_to_apiclip[1], _vertex);
    _r0017.z = dot(trans_model_to_apiclip[2], _vertex);
    _r0017.w = dot(trans_model_to_apiclip[3], _vertex);
    _l_texcoord01 = gl_MultiTexCoord0.xy;
    _r0027.x = dot(trans_model_to_view[0], _vertex);
    _r0027.y = dot(trans_model_to_view[1], _vertex);
    _r0027.z = dot(trans_model_to_view[2], _vertex);
    _r0027.w = dot(trans_model_to_view[3], _vertex);
    _r0037.x = dot(trans_view_to_world[0], _r0027);
    _r0037.y = dot(trans_view_to_world[1], _r0027);
    _l_interpolate1.xy = (_r0037.xy - map.xy)*map.zw;
    _l_alpha_uv1.xy = (_r0037.xy - alphamap.xy)*alphamap.zw;
    _x0047 = -(fogexpdensity.x*_r0027.y);
    _TMP46 = pow(2.71828198E+00, _x0047);
    _l_color1.w = 1.00000000E+00 - _TMP46;
    _r0051.x = dot(vec4( 5.00000000E-01, 0.00000000E+00, 0.00000000E+00, 5.00000000E-01), _r0017);
    _r0051.y = dot(vec4( 0.00000000E+00, 5.00000000E-01, 0.00000000E+00, 5.00000000E-01), _r0017);
    _r0051.w = dot(vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00), _r0017);
    _l_texcoord11.xy = _r0051.xy/_r0051.w;
    _v0061 = gl_Vertex.xyz - lightposition.xyz;
    _TMP2 = dot(_v0061, _v0061);
    _TMP3 = inversesqrt(_TMP2);
    _light_direction = _TMP3*_v0061;
    _v0067 = -_light_direction;
    _TMP2 = dot(_v0067, _v0067);
    _TMP3 = inversesqrt(_TMP2);
    _opposite_light_direction = _TMP3*_v0067;
    _diffuse = dot(gl_Normal, _opposite_light_direction);
    _l_color1.xyz = diffusecolor.xyz*_diffuse*lightparameters.x + ambientcolor.xyz;
    _l_position1 = _r0017;
    gl_TexCoord[2].xy = _l_interpolate1;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_TexCoord[3].xy = _l_alpha_uv1;
    gl_TexCoord[1].xy = _l_texcoord11;
    gl_Position = _r0017;
    gl_FrontColor = _l_color1;
} // main end
