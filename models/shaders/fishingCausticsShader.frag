//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.k_causticsParams
//semantic fshader.k_causticsParams2
//semantic fshader.k_causticsParams3
//semantic fshader.k_causticsToWorldScale
//semantic fshader.k_fogInfo
//semantic fshader.k_fogColor
//semantic fshader.k_timeInfo
//semantic fshader.tex_0 : TEXUNIT0
//semantic fshader.k_caustics : TEXUNIT1
//var float4 k_causticsParams :  : _k_causticsParams1 : 6 : 1
//\--replaced with causticsParams
//var float4 k_causticsParams2 :  : _k_causticsParams21 : 7 : 1
//\--replaced with causticsParams2
//var float4 k_causticsParams3 :  : _k_causticsParams31 : 8 : 1
//\--replaced with causticsParams3
//var float4 k_causticsToWorldScale :  : _k_causticsToWorldScale1 : 9 : 1
//\--replaced with causticsToWorldScale
//var float4 k_fogInfo :  : _k_fogInfo1 : 10 : 1
//\--replaced with fogInfo
//var float4 k_fogColor :  : _k_fogColor1 : 11 : 1
//\--replaced with fogColor
//var float4 k_timeInfo :  : _k_timeInfo1 : 12 : 1
//\--replaced with timeInfo
//var sampler2D tex_0 : TEXUNIT0 : _tex_01 0 : 13 : 1
//\--replaced with p3d_Texture0
//var sampler2D k_caustics : TEXUNIT1 : _k_caustics1 1 : 14 : 1
//\--replaced with caustics
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 0 : 1
//var float3 l_halfVec : $vin.TEXCOORD1 :  : 1 : 0
//var float4 l_eyevec : $vin.TEXCOORD2 : TEX2 : 2 : 1
//var float3 l_normal : $vin.TEXCOORD3 : TEX3 : 3 : 1
//var float4 l_worldPos : $vin.TEXCOORD4 : TEX4 : 4 : 1
//var float4 l_lightVec0 : $vin._l_lightVec01 : _l_lightVec01 : 5 : 1
//var float4 o_color : $vout.COLOR0 : COL : 15 : 1

#version 120

vec4 _o_color1;
float _TMP9;
float _TMP13;
vec3 _TMP12;
float _TMP7;
float _TMP6;
float _TMP11;
float _TMP10;
float _TMP1;
float _TMP0;
varying vec4 _l_lightVec01;
uniform vec4 causticsParams;
uniform vec4 causticsParams2;
uniform vec4 causticsParams3;
uniform vec4 causticsToWorldScale;
uniform vec4 fogInfo;
uniform vec4 fogColor;
uniform vec4 timeInfo;
uniform sampler2D p3d_Texture0;
uniform sampler2D caustics;
vec2 _c0027;
vec2 _c0029;
float _a0031;
float _a0033;
vec2 _c0035;
vec3 _x0053;
vec3 _TMP54;
float _x0073;
float _TMP74;
vec3 _a0087;

 // main procedure, the original name was fshader
void main()
{

    vec4 _baseColor;
    vec2 _causticsUVs;
    vec4 _causticsColor;
    vec4 _causticsColor2;
    vec4 _causticsColor3;
    vec3 _normal;
    vec3 _specularLight;

    _baseColor = texture2D(p3d_Texture0, gl_TexCoord[0].xy);
    _causticsUVs = gl_TexCoord[4].xy*causticsToWorldScale.xy;
    _c0027 = _causticsUVs.xy*causticsParams.x + causticsParams.yz*timeInfo.y;
    _causticsColor = texture2D(caustics, _c0027);
    _c0029 = _causticsUVs.xy*causticsParams2.x + causticsParams2.yz*timeInfo.y;
    _causticsColor2 = texture2D(caustics, _c0029);
    _a0031 = timeInfo.y*causticsParams3.y;
    _TMP0 = sin(_a0031);
    _a0033 = timeInfo.y*causticsParams3.z;
    _TMP1 = cos(_a0033);
    _c0035 = _causticsUVs.xy*causticsParams2.x + vec2(_TMP0, _TMP1);
    _causticsColor3 = texture2D(caustics, _c0035);
    _TMP10 = dot(gl_TexCoord[3].xyz, gl_TexCoord[3].xyz);
    _TMP11 = inversesqrt(_TMP10);
    _normal = _TMP11*gl_TexCoord[3].xyz;
    _x0053 = _causticsColor.xyz*causticsParams.w + _causticsColor2.xyz*causticsParams2.w + _causticsColor3.xyz*causticsParams3.w;
    _TMP12 = min(vec3( 1.00000000E+00, 1.00000000E+00, 1.00000000E+00), _x0053);
    _TMP54 = max(vec3( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00), _TMP12);
    _TMP6 = dot(_normal, _l_lightVec01.xyz);
    _TMP7 = max(0.00000000E+00, _TMP6);
    _specularLight = _TMP54*_TMP7;
    _x0073 = (gl_TexCoord[2].w - fogInfo.x)/(fogInfo.y - fogInfo.x);
    _TMP13 = min(1.00000000E+00, _x0073);
    _TMP74 = max(0.00000000E+00, _TMP13);
    _TMP9 = min(fogInfo.z, _TMP74);
    _a0087 = _baseColor.xyz + _specularLight;
    _o_color1.xyz = _a0087 + _TMP9*(fogColor.xyz - _a0087);
    _o_color1.w = _baseColor.w;
    gl_FragColor = _o_color1;
} // main end
