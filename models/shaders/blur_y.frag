//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.tex_0 : TEXUNIT0
//var sampler2D tex_0 : TEXUNIT0 : _tex_01 0 : 2 : 1
//\--replaced with p3d_Texture0
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 0 : 1
//var float4 o_color : $vout.COLOR : COL : 1 : 1

#version 120

vec4 _o_color1;
vec4 _TMP5;
vec4 _TMP4;
vec4 _TMP3;
vec4 _TMP2;
vec4 _TMP1;
vec4 _TMP0;
uniform sampler2D p3d_Texture0;
vec2 _c0008;
vec2 _c0010;
vec2 _c0012;
vec2 _c0014;
vec2 _c0016;
vec2 _c0018;

 // main procedure, the original name was fshader
void main()
{


    _c0008 = vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 8.78906250E-03);
    _TMP0 = texture2D(p3d_Texture0, _c0008);
    _o_color1 = _TMP0*5.00000000E+00;
    _c0010 = vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 4.88281250E-03);
    _TMP1 = texture2D(p3d_Texture0, _c0010);
    _o_color1 = _o_color1 + _TMP1*8.00000000E+00;
    _c0012 = vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 9.76562500E-04);
    _TMP2 = texture2D(p3d_Texture0, _c0012);
    _o_color1 = _o_color1 + _TMP2*1.00000000E+01;
    _c0014 = vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 9.76562500E-04);
    _TMP3 = texture2D(p3d_Texture0, _c0014);
    _o_color1 = _o_color1 + _TMP3*1.00000000E+01;
    _c0016 = vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 4.88281250E-03);
    _TMP4 = texture2D(p3d_Texture0, _c0016);
    _o_color1 = _o_color1 + _TMP4*8.00000000E+00;
    _c0018 = vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 8.78906250E-03);
    _TMP5 = texture2D(p3d_Texture0, _c0018);
    _o_color1 = _o_color1 + _TMP5*5.00000000E+00;
    _o_color1 = _o_color1*2.99999993E-02;
    gl_FragColor = _o_color1;
} // main end
