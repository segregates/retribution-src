//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.k_fogcolor
//semantic fshader.k_reflectionparameters
//semantic fshader.k_watercolortexture
//semantic fshader.k_reflectiontexture
//semantic fshader.k_wateralphatexture
//var float4 k_fogcolor :  : _k_fogcolor1 : 4 : 1
//\--replaced with fogcolor
//var float4 k_reflectionparameters :  : _k_reflectionparameters1 : 5 : 1
//\--replaced with reflectionparameters
//var sampler2D k_watercolortexture :  : _k_watercolortexture1 : 6 : 1
//\--replaced with watercolortexture
//var sampler2D k_reflectiontexture :  : _k_reflectiontexture1 : 7 : 1
//\--replaced with reflectiontexture
//var sampler2D k_wateralphatexture :  : _k_wateralphatexture1 : 8 : 1
//\--replaced with wateralphatexture
//var float2 l_texcoord1 : $vin.TEXCOORD1 : TEX1 : 0 : 1
//var float2 l_interpolate : $vin.TEXCOORD2 : TEX2 : 1 : 1
//var float2 l_alpha_uv : $vin.TEXCOORD3 : TEX3 : 2 : 1
//var float4 l_color : $vin.COLOR0 : COL0 : 3 : 1
//var float4 o_color : $vout.COLOR : COL : 9 : 1

#version 120

vec4 _o_color1;
vec4 _TMP0;
uniform vec4 fogcolor;
uniform vec4 reflectionparameters;
uniform sampler2D watercolortexture;
uniform sampler2D reflectiontexture;
uniform sampler2D wateralphatexture;

 // main procedure, the original name was fshader
void main()
{

    vec4 _water_color;
    vec4 _reflection_texel;
    vec4 _output_color;

    _water_color = texture2D(watercolortexture, gl_TexCoord[2].xy);
    _reflection_texel = texture2D(reflectiontexture, gl_TexCoord[1].xy);
    _output_color = gl_Color*_water_color;
    _output_color.xyz = _output_color.xyz + reflectionparameters.z*_reflection_texel.xyz;
    _output_color.xyz = _output_color.xyz + gl_Color.w*(fogcolor.xyz - _output_color.xyz);
    _TMP0 = texture2D(wateralphatexture, gl_TexCoord[3].xy);
    _output_color.w = 1.00000000E+00 - _TMP0.x;
    _o_color1 = _output_color;
    gl_FragColor = _output_color;
} // main end
