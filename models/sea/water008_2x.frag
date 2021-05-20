//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.k_fogcolor
//semantic fshader.k_uvanim
//semantic fshader.k_lightposition
//semantic fshader.k_cameraposition
//semantic fshader.k_ambientcolor
//semantic fshader.k_diffusecolor
//semantic fshader.k_specularcolor
//semantic fshader.k_lightparameters
//semantic fshader.k_watercolor
//semantic fshader.k_reflectionparameters
//semantic fshader.k_watercolorfactor
//semantic fshader.k_watercoloradd
//semantic fshader.k_fogexpdensity
//semantic fshader.tex_0
//semantic fshader.tex_0_d
//semantic fshader.tex_0_n
//semantic fshader.tex_0_bb
//semantic fshader.tex_0_low2
//semantic fshader.k_watercolortexture
//semantic fshader.k_reflectiontexture
//semantic fshader.k_wateralphatexture
//var float4 k_fogcolor :  : _k_fogcolor1 : 6 : 1
//\--replaced with fogcolor
//var float4 k_uvanim :  : _k_uvanim1 : 7 : 1
//\--replaced with uvanim
//var float4 k_lightposition :  : _k_lightposition1 : 8 : 1
//\--replaced with lightposition
//var float4 k_cameraposition :  : _k_cameraposition1 : 9 : 1
//\--replaced with cameraposition
//var float4 k_ambientcolor :  : _k_ambientcolor1 : 10 : 1
//\--replaced with ambientcolor
//var float4 k_diffusecolor :  : _k_diffusecolor1 : 11 : 1
//\--replaced with diffusecolor
//var float4 k_specularcolor :  : _k_specularcolor1 : 12 : 1
//\--replaced with specularcolor
//var float4 k_lightparameters :  : _k_lightparameters1 : 13 : 1
//\--replaced with lightparameters
//var float4 k_reflectionparameters :  : _k_reflectionparameters1 : 15 : 1
//\--replaced with reflectionparameters
//var float4 k_watercolorfactor :  : _k_watercolorfactor1 : 16 : 1
//\--replaced with watercolorfactor
//var float4 k_watercoloradd :  : _k_watercoloradd1 : 17 : 1
//\--replaced with watercoloradd
//var float4 k_fogexpdensity :  : _k_fogexpdensity1 : 18 : 1
//\--replaced with fogexpdensity
//var sampler2D tex_0_d :  : _tex_0_d1 : 20 : 1
//\--replaced with p3d_Texture0_d
//var sampler2D tex_0_n :  : _tex_0_n1 : 21 : 1
//\--replaced with p3d_Texture0_n
//var sampler2D tex_0_bb :  : _tex_0_bb1 : 22 : 1
//\--replaced with p3d_Texture0_bb
//var sampler2D tex_0_low2 :  : _tex_0_low21 : 23 : 1
//\--replaced with p3d_Texture0_low2
//var sampler2D k_watercolortexture :  : _k_watercolortexture1 : 24 : 1
//\--replaced with watercolortexture
//var sampler2D k_reflectiontexture :  : _k_reflectiontexture1 : 25 : 1
//\--replaced with reflectiontexture
//var sampler2D k_wateralphatexture :  : _k_wateralphatexture1 : 26 : 1
//\--replaced with wateralphatexture
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 0 : 1
//var float4 l_texcoord1 : $vin.TEXCOORD1 : TEX1 : 1 : 1
//var float3 l_normal : $vin.TEXCOORD2 : TEX2 : 2 : 1
//var float3 l_surface_pos : $vin.TEXCOORD3 : TEX3 : 3 : 1
//var float3 l_interpolate : $vin.TEXCOORD4 : TEX4 : 4 : 1
//var float2 l_alpha_uv : $vin.TEXCOORD5 : TEX5 : 5 : 1
//var float4 o_color : $vout.COLOR : COL : 27 : 1

#version 120

vec4 _o_color1;
vec4 _TMP13;
float _TMP11;
float _TMP10;
float _TMP9;
float _TMP16;
float _TMP15;
float _TMP14;
float _TMP8;
float _TMP6;
vec2 _TMP17;
float _TMP5;
float _TMP3;
vec4 _TMP2;
vec4 _TMP1;
vec4 _TMP0;
uniform vec4 fogcolor;
uniform vec4 uvanim;
uniform vec4 lightposition;
uniform vec4 cameraposition;
uniform vec4 ambientcolor;
uniform vec4 diffusecolor;
uniform vec4 specularcolor;
uniform vec4 lightparameters;
uniform vec4 reflectionparameters;
uniform vec4 watercolorfactor;
uniform vec4 watercoloradd;
uniform vec4 fogexpdensity;
uniform sampler2D p3d_Texture0_d;
uniform sampler2D p3d_Texture0_n;
uniform sampler2D p3d_Texture0_bb;
uniform sampler2D p3d_Texture0_low2;
uniform sampler2D watercolortexture;
uniform sampler2D reflectiontexture;
uniform sampler2D wateralphatexture;
vec2 _c0040;
vec2 _c0042;
vec2 _c0044;
vec2 _c0046;
vec3 _v0048;
vec3 _v0054;
vec3 _v0068;
float _TMP77;
vec2 _TMP89;
vec3 _v0098;
vec3 _v0104;
vec3 _v0110;
vec3 _v0130;
float _TMP139;
vec3 _v0148;
vec3 _v0154;
vec3 _v0162;
vec3 _v0168;
float _TMP177;
float _TMP187;
float _x0188;
float _t0192;

 // main procedure, the original name was fshader
void main()
{

    float _diffuse;
    float _specular;
    vec3 _world_normal;
    vec3 _light_direction;
    vec3 _opposite_light_direction;
    vec3 _reflection_vector;
    vec4 _colormap_d;
    vec4 _normalmap;
    vec4 _normalmap2;
    vec4 _normalmap3;
    vec4 _base_water_color;
    vec4 _water_color;
    vec4 _reflection_texel;
    vec2 _projection_uv1;
    vec3 _surface_to_camera_vector;
    vec3 _camera_position;
    vec3 _surface_normal;
    vec4 _output_color;
    vec3 _surface_to_camera_vector21;
    float _z_factor1;
    float _y_factor1;

    _c0040 = (gl_TexCoord[0].xy + uvanim.xy)*2.00000000E+00;
    _colormap_d = texture2D(p3d_Texture0_d, _c0040);
    _c0042 = gl_TexCoord[0].xy + uvanim.zw;
    _TMP0 = texture2D(p3d_Texture0_n, _c0042);
    _normalmap = _TMP0*2.00000000E+00 - 1.00000000E+00;
    _c0044 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP1 = texture2D(p3d_Texture0_bb, _c0044);
    _normalmap2 = _TMP1*2.00000000E+00 - 1.00000000E+00;
    _c0046 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP2 = texture2D(p3d_Texture0_low2, _c0046);
    _normalmap3 = _TMP2 - 1.00000000E+00;
    _v0048 = vec3( 0.00000000E+00, -2.00000000E+02, -1.00000000E+03) - gl_TexCoord[3].xyz;
    _TMP14 = dot(_v0048, _v0048);
    _TMP15 = inversesqrt(_TMP14);
    _light_direction = _TMP15*_v0048;
    _v0054 = -_light_direction;
    _TMP14 = dot(_v0054, _v0054);
    _TMP15 = inversesqrt(_TMP14);
    _opposite_light_direction = _TMP15*_v0054;
    _world_normal.xyz = _normalmap.xzy*1.00000001E-01 + _normalmap2.xzy*2.50000000E-01 + gl_TexCoord[2].xyz*6.99999988E-01;
    _TMP14 = dot(_world_normal, _world_normal);
    _TMP15 = inversesqrt(_TMP14);
    _world_normal = _TMP15*_world_normal;
    _diffuse = dot(_world_normal, _opposite_light_direction);
    _v0068 = (2.00000000E+00*_diffuse)*_world_normal - _opposite_light_direction;
    _TMP14 = dot(_v0068, _v0068);
    _TMP15 = inversesqrt(_TMP14);
    _reflection_vector = _TMP15*_v0068;
    _TMP3 = dot(_reflection_vector, _opposite_light_direction);
    _TMP16 = min(1.00000000E+00, _TMP3);
    _TMP77 = max(0.00000000E+00, _TMP16);
    _TMP5 = pow(_TMP77, 2.00000000E+01);
    _specular = 7.50000030E-02*_TMP5;
    _diffuse = _diffuse*3.49999994E-01;
    if (_diffuse < 0.00000000E+00) { // if begin
        _diffuse = 0.00000000E+00;
        _specular = 0.00000000E+00;
    } // end if
    _base_water_color = texture2D(watercolortexture, gl_TexCoord[4].xy);
    _base_water_color.xyz = _base_water_color.xyz*watercolorfactor.xyz + watercoloradd.xyz;
    _base_water_color.xyz = _base_water_color.xyz*1.50000000E+00;
    _water_color = (_colormap_d*1.00000001E-01 + _diffuse*_base_water_color) + _specular;
    _projection_uv1 = gl_TexCoord[1].xy/gl_TexCoord[1].w;
    _projection_uv1 = _projection_uv1 + reflectionparameters.w*((_normalmap3.xy - _normalmap3.yx)*reflectionparameters.xy) + (1.00000000E+00 - reflectionparameters.w)*((_normalmap2.xy - _normalmap2.yx)*reflectionparameters.xy);
    _TMP17 = min(vec2( 1.00000000E+00, 1.00000000E+00), _projection_uv1);
    _TMP89 = max(vec2( 0.00000000E+00, 0.00000000E+00), _TMP17);
    _reflection_texel = texture2D(reflectiontexture, _TMP89);
    _camera_position.x = 0.00000000E+00;
    _camera_position.y = 0.00000000E+00;
    _camera_position.z = cameraposition.z;
    _v0098 = _camera_position.xyz - gl_TexCoord[3].xyz;
    _TMP14 = dot(_v0098, _v0098);
    _TMP15 = inversesqrt(_TMP14);
    _surface_to_camera_vector = _TMP15*_v0098;
    _v0104 = gl_TexCoord[3].xyz - lightposition.xyz;
    _TMP14 = dot(_v0104, _v0104);
    _TMP15 = inversesqrt(_TMP14);
    _light_direction = _TMP15*_v0104;
    _v0110 = -_light_direction;
    _TMP14 = dot(_v0110, _v0110);
    _TMP15 = inversesqrt(_TMP14);
    _opposite_light_direction = _TMP15*_v0110;
    _TMP14 = dot(vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00), vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00));
    _TMP15 = inversesqrt(_TMP14);
    _surface_normal = _TMP15*vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00);
    _surface_normal = _surface_normal + gl_TexCoord[2].xyz*1.00000001E-01 + _normalmap2.xyz*5.00000007E-02;
    _TMP14 = dot(_surface_normal, _surface_normal);
    _TMP15 = inversesqrt(_TMP14);
    _surface_normal = _TMP15*_surface_normal;
    _diffuse = dot(_surface_normal, _opposite_light_direction);
    _v0130 = (2.00000000E+00*_diffuse)*_surface_normal - _opposite_light_direction;
    _TMP14 = dot(_v0130, _v0130);
    _TMP15 = inversesqrt(_TMP14);
    _reflection_vector = _TMP15*_v0130;
    _TMP6 = dot(_reflection_vector, _surface_to_camera_vector);
    _TMP16 = min(1.00000000E+00, _TMP6);
    _TMP139 = max(0.00000000E+00, _TMP16);
    _TMP8 = pow(_TMP139, lightparameters.z);
    _specular = lightparameters.y*_TMP8;
    _diffuse = _diffuse*lightparameters.x;
    if (_diffuse < 0.00000000E+00) { // if begin
        _diffuse = 0.00000000E+00;
        _specular = 0.00000000E+00;
    } // end if
    if (_reflection_texel.w > 0.00000000E+00) { // if begin
        _specular = 0.00000000E+00;
    } // end if
    _output_color = ambientcolor*_water_color + (_diffuse*diffusecolor)*_water_color + _specular*specularcolor;
    _v0148 = vec3( 0.00000000E+00, -4.10000000E+03, 1.36000000E+04) - gl_TexCoord[3].xyz;
    _TMP14 = dot(_v0148, _v0148);
    _TMP15 = inversesqrt(_TMP14);
    _opposite_light_direction = _TMP15*_v0148;
    _v0154 = gl_TexCoord[2].xyz + _normalmap2.xyz*2.00000003E-01;
    _TMP14 = dot(_v0154, _v0154);
    _TMP15 = inversesqrt(_TMP14);
    _surface_normal = _TMP15*_v0154;
    _diffuse = dot(_surface_normal, _opposite_light_direction);
    _v0162 = vec3( 0.00000000E+00, 0.00000000E+00, -5.00000000E+00) - gl_TexCoord[3].xyz;
    _TMP14 = dot(_v0162, _v0162);
    _TMP15 = inversesqrt(_TMP14);
    _surface_to_camera_vector21 = _TMP15*_v0162;
    _v0168 = (2.00000000E+00*_diffuse)*_surface_normal - _opposite_light_direction;
    _TMP14 = dot(_v0168, _v0168);
    _TMP15 = inversesqrt(_TMP14);
    _reflection_vector = _TMP15*_v0168;
    _TMP9 = dot(_reflection_vector, _surface_to_camera_vector21);
    _TMP16 = min(1.00000000E+00, _TMP9);
    _TMP177 = max(0.00000000E+00, _TMP16);
    _TMP10 = min(cameraposition.z, 5.00000000E+02);
    _z_factor1 = (5.00000000E+02 - _TMP10)/5.00000000E+02;
    _TMP11 = min(gl_TexCoord[3].y, 3.50000000E+02);
    _y_factor1 = (3.50000000E+02 - _TMP11)/3.50000000E+02;
    _output_color.xyz = _output_color.xyz + _TMP177*_z_factor1*_y_factor1;
    _output_color.xyz = _output_color.xyz + reflectionparameters.z*_reflection_texel.xyz;
    _x0188 = -(fogexpdensity.x*gl_TexCoord[4].z);
    _TMP187 = pow(2.71828198E+00, _x0188);
    _t0192 = 1.00000000E+00 - _TMP187;
    _output_color.xyz = _output_color.xyz + _t0192*(fogcolor.xyz - _output_color.xyz);
    _TMP13 = texture2D(wateralphatexture, gl_TexCoord[5].xy);
    _output_color.w = 1.00000000E+00 - _TMP13.x;
    _o_color1 = _output_color;
    gl_FragColor = _output_color;
} // main end
