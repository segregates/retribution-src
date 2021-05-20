//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.k_parameters
//semantic fshader.tex_0 : TEXUNIT0
//var float4 k_parameters :  : _k_parameters1 : 0 : 1
//\--replaced with parameters
//var sampler2D tex_0 : TEXUNIT0 : _tex_01 0 : 3 : 1
//\--replaced with p3d_Texture0
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 1 : 1
//var float4 o_color : $vout.COLOR : COL : 2 : 1

#version 120

vec4 _o_color1;
vec4 _TMP3;
vec4 _TMP2;
vec4 _TMP1;
vec4 _TMP0;
uniform vec4 parameters;
uniform sampler2D p3d_Texture0;
vec2 _c0007;
vec2 _c0009;
vec2 _c0011;
vec2 _c0013;

 // main procedure, the original name was fshader
void main()
{

    vec4 _color;
    vec4 _x_offsets;
    vec4 _y_offsets;

    _x_offsets = gl_TexCoord[0].x + parameters.x*vec4( 0.00000000E+00, 2.00000000E+00, 0.00000000E+00, 0.00000000E+00);
    _y_offsets = gl_TexCoord[0].y + parameters.y*vec4( 0.00000000E+00, 2.00000000E+00, 0.00000000E+00, 0.00000000E+00);
    _c0007 = vec2(_x_offsets.x, _y_offsets.x);
    _TMP0 = texture2D(p3d_Texture0, _c0007);
    _c0009 = vec2(_x_offsets.y, _y_offsets.x);
    _TMP1 = texture2D(p3d_Texture0, _c0009);
    _color = _TMP0 + _TMP1;
    _c0011 = vec2(_x_offsets.x, _y_offsets.y);
    _TMP2 = texture2D(p3d_Texture0, _c0011);
    _color = _color + _TMP2;
    _c0013 = vec2(_x_offsets.y, _y_offsets.y);
    _TMP3 = texture2D(p3d_Texture0, _c0013);
    _color = _color + _TMP3;
    _color = _color*2.50000000E-01;
    _color.w = 1.00000000E+00;
    _o_color1 = _color;
    gl_FragColor = _color;
} // main end
