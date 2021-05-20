//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.k_parameters
//semantic fshader.k_factors
//semantic fshader.k_parameters2
//semantic fshader.tex_0 : TEXUNIT0
//semantic fshader.k_original : TEXUNIT1
//semantic fshader.k_average : TEXUNIT2
//var float4 k_parameters :  : _k_parameters1 : 0 : 1
//\--replaced with parameters
//var float4 k_factors :  : _k_factors1 : 1 : 1
//\--replaced with factors
//var float4 k_parameters2 :  : _k_parameters21 : 2 : 1
//\--replaced with parameters2
//var sampler2D tex_0 : TEXUNIT0 : _tex_01 0 : 5 : 1
//\--replaced with p3d_Texture0
//var sampler2D k_original : TEXUNIT1 : _k_original1 1 : 6 : 1
//\--replaced with original
//var sampler2D k_average : TEXUNIT2 : _k_average1 2 : 7 : 1
//\--replaced with average
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 3 : 1
//var float4 o_color : $vout.COLOR : COL : 4 : 1

#version 120

vec4 _o_color1;
float _TMP2;
float _TMP1;
float _TMP0;
uniform vec4 parameters;
uniform vec4 factors;
uniform vec4 parameters2;
uniform sampler2D p3d_Texture0;
uniform sampler2D original;
uniform sampler2D average;

 // main procedure, the original name was fshader
void main()
{

    vec4 _color;
    vec4 _original_color;
    vec4 _blurred_color;
    float _c_exposure;
    float _c_exposure2;
    float _exposure1;
    vec4 _average_color1;
    float _luminance1;

    _c_exposure = parameters.x;
    _c_exposure2 = parameters.z;
    if (parameters.w > 0.00000000E+00) { // if begin
        _average_color1 = texture2D(average, vec2( 0.00000000E+00, 0.00000000E+00));
        _luminance1 = dot(_average_color1.xyz, vec3( 2.12500006E-01, 7.15399981E-01, 7.20999986E-02));
        _exposure1 = 5.00000000E-01/_luminance1;
        if (_exposure1 < factors.z) { // if begin
            _exposure1 = factors.z;
        } // end if
        if (_exposure1 > factors.w) { // if begin
            _exposure1 = factors.w;
        } // end if
        _c_exposure = _exposure1;
        _c_exposure2 = _exposure1;
    } // end if
    _original_color = texture2D(original, gl_TexCoord[0].xy);
    if (gl_TexCoord[0].x < 5.00000000E-01) { // if begin
        _color.xyz = _original_color.xyz;
    } else {
        _blurred_color = texture2D(p3d_Texture0, gl_TexCoord[0].xy);
        _blurred_color.xyz = _blurred_color.xyz*_c_exposure2;
        _color.xyz = _original_color.xyz*_c_exposure*factors.x + _blurred_color.xyz*factors.y;
        _color.xyz = _original_color.xyz + parameters2.x*(_color.xyz - _original_color.xyz);
    } // end if
    _TMP0 = pow(_color.x, parameters.y);
    _TMP1 = pow(_color.y, parameters.y);
    _TMP2 = pow(_color.z, parameters.y);
    _color.xyz = vec3(_TMP0, _TMP1, _TMP2);
    _color.w = 1.00000000E+00;
    _o_color1 = _color;
    gl_FragColor = _color;
} // main end
