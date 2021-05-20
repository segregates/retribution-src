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
uniform sampler2D p3d_Texture0;

 // main procedure, the original name was fshader
void main()
{

    vec4 _color;
    float _luminance;

    _color = texture2D(p3d_Texture0, gl_TexCoord[0].xy);
    _luminance = dot(_color.xyz, vec3( 2.12500006E-01, 7.15399981E-01, 7.20999986E-02));
    if (_luminance >= 0.00000000E+00) { // if begin
        _o_color1.xyz = _color.xyz*_luminance*7.50000000E-01;
    } else {
        _o_color1.xyz = _color.xyz*3.30000013E-01;
    } // end if
    _o_color1.w = 1.00000000E+00;
    gl_FragColor = _o_color1;
} // main end
