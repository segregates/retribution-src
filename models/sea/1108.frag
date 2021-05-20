#version 120

vec4 _TMP0;
uniform vec4 fogcolor;
uniform vec4 reflectionparameters;
uniform vec4 p3d_Color;
uniform sampler2D watercolortexture;
uniform sampler2D reflectiontexture;
uniform sampler2D wateralphatexture;

void main()
{

    vec4 _water_color;
    vec4 _reflection_texel;
    vec4 _output_color;
    _water_color = p3d_Color;
    _reflection_texel = texture2D(reflectiontexture, gl_TexCoord[1].xy);
    _output_color = _water_color;
    _output_color.xyz = _output_color.xyz + reflectionparameters.z*_reflection_texel.xyz;
    _output_color.xyz = _output_color.xyz + gl_Color.w*(fogcolor.xyz - _output_color.xyz);
    _TMP0 = texture2D(wateralphatexture, gl_TexCoord[3].xy);
    _output_color.w = 1.00000000E+00 - _TMP0.x;
    gl_FragColor = _output_color;
}
