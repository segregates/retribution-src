//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.k_glowfactor
//semantic fshader.tex_0 : TEXUNIT0
//semantic fshader.k_glow : TEXUNIT1
//var float4 k_glowfactor :  : _k_glowfactor1 : 0 : 1
//\--replaced with glowfactor
//var sampler2D tex_0 : TEXUNIT0 : _tex_01 0 : 3 : 1
//\--replaced with p3d_Texture0
//var sampler2D k_glow : TEXUNIT1 : _k_glow1 1 : 4 : 1
//\--replaced with glow
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 1 : 1
//var float4 o_color : $vout.COLOR : COL : 2 : 1

#version 120

vec4 _o_color1;
uniform vec4 glowfactor;
uniform sampler2D p3d_Texture0;
uniform sampler2D glow;

 // main procedure, the original name was fshader
void main()
{

    vec4 _color;
    vec4 _glow_color;
    float _luminance;

    _color = texture2D(p3d_Texture0, gl_TexCoord[0].xy);
    _glow_color = texture2D(glow, gl_TexCoord[0].xy);
    _luminance = dot(_color.xyz, vec3( 2.12500006E-01, 7.15399981E-01, 7.20999986E-02));
    if (_luminance >= 0.00000000E+00) { // if begin
        _color.xyz = _color.xyz*_luminance*7.50000000E-01;
    } else {
        _color.xyz = _color.xyz*3.30000013E-01;
    } // end if
    _color.xyz = _color.xyz + _glow_color.xyz*glowfactor.x;
    _o_color1.xyz = _color.xyz;
    _o_color1.w = 1.00000000E+00;
    gl_FragColor = _o_color1;
} // main end
