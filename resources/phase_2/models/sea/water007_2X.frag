//vendor NVIDIA Corporation
//version 3.1.0.13
//profile glslf
//program fshader
//semantic fshader.k_fogcolor : C1
//semantic fshader.k_uvanim : C2
//semantic fshader.k_lightposition : C3
//semantic fshader.k_cameraposition : C4
//semantic fshader.k_ambientcolor : C5
//semantic fshader.k_diffusecolor : C6
//semantic fshader.k_specularcolor : C7
//semantic fshader.k_lightparameters : C8
//semantic fshader.k_watercolor : C9
//semantic fshader.k_reflectionparameters : C10
//semantic fshader.tex_0
//semantic fshader.tex_0_d
//semantic fshader.tex_0_n
//semantic fshader.tex_0_bb
//semantic fshader.tex_0_low2
//semantic fshader.k_watercolortexture
//semantic fshader.k_reflectiontexture
//semantic fshader.k_wateralphatexture
//var float4 k_fogcolor : C1 : _k_fogcolor1 : 6 : 1
//\--replaced with fogcolor
//var float4 k_uvanim : C2 : _k_uvanim1 : 7 : 1
//\--replaced with uvanim
//var float4 k_lightposition : C3 : _k_lightposition1 : 8 : 1
//\--replaced with lightposition
//var float4 k_cameraposition : C4 : _k_cameraposition1 : 9 : 1
//\--replaced with cameraposition
//var float4 k_ambientcolor : C5 : _k_ambientcolor1 : 10 : 1
//\--replaced with ambientcolor
//var float4 k_diffusecolor : C6 : _k_diffusecolor1 : 11 : 1
//\--replaced with diffusecolor
//var float4 k_specularcolor : C7 : _k_specularcolor1 : 12 : 1
//\--replaced with specularcolor
//var float4 k_lightparameters : C8 : _k_lightparameters1 : 13 : 1
//\--replaced with lightparameters
//var float4 k_reflectionparameters : C10 : _k_reflectionparameters1 : 15 : 1
//\--replaced with reflectionparameters
//var sampler2D tex_0_d :  : _tex_0_d1 : 17 : 1
//\--replaced with p3d_Texture0_d
//var sampler2D tex_0_n :  : _tex_0_n1 : 18 : 1
//\--replaced with p3d_Texture0_n
//var sampler2D tex_0_bb :  : _tex_0_bb1 : 19 : 1
//\--replaced with p3d_Texture0_bb
//var sampler2D tex_0_low2 :  : _tex_0_low21 : 20 : 1
//\--replaced with p3d_Texture0_low2
//var sampler2D k_watercolortexture :  : _k_watercolortexture1 : 21 : 1
//\--replaced with watercolortexture
//var sampler2D k_reflectiontexture :  : _k_reflectiontexture1 : 22 : 1
//\--replaced with reflectiontexture
//var sampler2D k_wateralphatexture :  : _k_wateralphatexture1 : 23 : 1
//\--replaced with wateralphatexture
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 0 : 1
//var float4 l_texcoord1 : $vin.TEXCOORD1 : TEX1 : 1 : 1
//var float3 l_normal : $vin.TEXCOORD2 : TEX2 : 2 : 1
//var float3 l_surface_pos : $vin.TEXCOORD3 : TEX3 : 3 : 1
//var float3 l_interpolate : $vin.TEXCOORD4 : TEX4 : 4 : 1
//var float2 l_alpha_uv : $vin.TEXCOORD5 : TEX5 : 5 : 1
//var float4 o_color : $vout.COLOR : COL : 24 : 1

#version 120

vec4 _o_color1;
vec4 _TMP12;
float _TMP11;
float _TMP10;
float _TMP9;
float _TMP15;
float _TMP14;
float _TMP13;
float _TMP8;
float _TMP6;
vec2 _TMP16;
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
uniform sampler2D p3d_Texture0_d;
uniform sampler2D p3d_Texture0_n;
uniform sampler2D p3d_Texture0_bb;
uniform sampler2D p3d_Texture0_low2;
uniform sampler2D watercolortexture;
uniform sampler2D reflectiontexture;
uniform sampler2D wateralphatexture;
vec2 _c0036;
vec2 _c0038;
vec2 _c0040;
vec2 _c0042;
vec3 _v0044;
vec3 _v0050;
vec3 _v0064;
float _TMP73;
vec2 _TMP85;
vec3 _v0094;
vec3 _v0100;
vec3 _v0106;
vec3 _v0126;
float _TMP135;
vec3 _v0144;
vec3 _v0150;
vec3 _v0158;
vec3 _v0164;
float _TMP173;

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

    _c0036 = (gl_TexCoord[0].xy + uvanim.xy)*2.00000000E+00;
    _colormap_d = texture2D(p3d_Texture0_d, _c0036);
    _c0038 = gl_TexCoord[0].xy + uvanim.zw;
    _TMP0 = texture2D(p3d_Texture0_n, _c0038);
    _normalmap = _TMP0*2.00000000E+00 - 1.00000000E+00;
    _c0040 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP1 = texture2D(p3d_Texture0_bb, _c0040);
    _normalmap2 = _TMP1*2.00000000E+00 - 1.00000000E+00;
    _c0042 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP2 = texture2D(p3d_Texture0_low2, _c0042);
    _normalmap3 = _TMP2 - 1.00000000E+00;
    _v0044 = vec3( 0.00000000E+00, -2.00000000E+02, -1.00000000E+03) - gl_TexCoord[3].xyz;
    _TMP13 = dot(_v0044, _v0044);
    _TMP14 = inversesqrt(_TMP13);
    _light_direction = _TMP14*_v0044;
    _v0050 = -_light_direction;
    _TMP13 = dot(_v0050, _v0050);
    _TMP14 = inversesqrt(_TMP13);
    _opposite_light_direction = _TMP14*_v0050;
    _world_normal.xyz = _normalmap.xzy*1.00000001E-01 + _normalmap2.xzy*2.50000000E-01 + gl_TexCoord[2].xyz*6.99999988E-01;
    _TMP13 = dot(_world_normal, _world_normal);
    _TMP14 = inversesqrt(_TMP13);
    _world_normal = _TMP14*_world_normal;
    _diffuse = dot(_world_normal, _opposite_light_direction);
    _v0064 = (2.00000000E+00*_diffuse)*_world_normal - _opposite_light_direction;
    _TMP13 = dot(_v0064, _v0064);
    _TMP14 = inversesqrt(_TMP13);
    _reflection_vector = _TMP14*_v0064;
    _TMP3 = dot(_reflection_vector, _opposite_light_direction);
    _TMP15 = min(1.00000000E+00, _TMP3);
    _TMP73 = max(0.00000000E+00, _TMP15);
    _TMP5 = pow(_TMP73, 2.00000000E+01);
    _specular = 7.50000030E-02*_TMP5;
    _diffuse = _diffuse*3.49999994E-01;
    if (_diffuse < 0.00000000E+00) { // if begin
        _diffuse = 0.00000000E+00;
        _specular = 0.00000000E+00;
    } // end if
    _base_water_color = texture2D(watercolortexture, gl_TexCoord[4].xy);
    _base_water_color.xyz = _base_water_color.xyz*1.50000000E+00;
    _water_color = (_colormap_d*1.00000001E-01 + _diffuse*_base_water_color) + _specular;
    _projection_uv1 = gl_TexCoord[1].xy/gl_TexCoord[1].w;
    _projection_uv1 = _projection_uv1 + reflectionparameters.w*((_normalmap3.xy - _normalmap3.yx)*reflectionparameters.xy) + (1.00000000E+00 - reflectionparameters.w)*((_normalmap2.xy - _normalmap2.yx)*reflectionparameters.xy);
    _TMP16 = min(vec2( 1.00000000E+00, 1.00000000E+00), _projection_uv1);
    _TMP85 = max(vec2( 0.00000000E+00, 0.00000000E+00), _TMP16);
    _reflection_texel = texture2D(reflectiontexture, _TMP85);
    _camera_position.x = 0.00000000E+00;
    _camera_position.y = 0.00000000E+00;
    _camera_position.z = cameraposition.z;
    _v0094 = _camera_position.xyz - gl_TexCoord[3].xyz;
    _TMP13 = dot(_v0094, _v0094);
    _TMP14 = inversesqrt(_TMP13);
    _surface_to_camera_vector = _TMP14*_v0094;
    _v0100 = gl_TexCoord[3].xyz - lightposition.xyz;
    _TMP13 = dot(_v0100, _v0100);
    _TMP14 = inversesqrt(_TMP13);
    _light_direction = _TMP14*_v0100;
    _v0106 = -_light_direction;
    _TMP13 = dot(_v0106, _v0106);
    _TMP14 = inversesqrt(_TMP13);
    _opposite_light_direction = _TMP14*_v0106;
    _TMP13 = dot(vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00), vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00));
    _TMP14 = inversesqrt(_TMP13);
    _surface_normal = _TMP14*vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00);
    _surface_normal = _surface_normal + gl_TexCoord[2].xyz*1.00000001E-01 + _normalmap2.xyz*5.00000007E-02;
    _TMP13 = dot(_surface_normal, _surface_normal);
    _TMP14 = inversesqrt(_TMP13);
    _surface_normal = _TMP14*_surface_normal;
    _diffuse = dot(_surface_normal, _opposite_light_direction);
    _v0126 = (2.00000000E+00*_diffuse)*_surface_normal - _opposite_light_direction;
    _TMP13 = dot(_v0126, _v0126);
    _TMP14 = inversesqrt(_TMP13);
    _reflection_vector = _TMP14*_v0126;
    _TMP6 = dot(_reflection_vector, _surface_to_camera_vector);
    _TMP15 = min(1.00000000E+00, _TMP6);
    _TMP135 = max(0.00000000E+00, _TMP15);
    _TMP8 = pow(_TMP135, lightparameters.z);
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
    _v0144 = vec3( 0.00000000E+00, -4.10000000E+03, 1.36000000E+04) - gl_TexCoord[3].xyz;
    _TMP13 = dot(_v0144, _v0144);
    _TMP14 = inversesqrt(_TMP13);
    _opposite_light_direction = _TMP14*_v0144;
    _v0150 = gl_TexCoord[2].xyz + _normalmap2.xyz*2.00000003E-01;
    _TMP13 = dot(_v0150, _v0150);
    _TMP14 = inversesqrt(_TMP13);
    _surface_normal = _TMP14*_v0150;
    _diffuse = dot(_surface_normal, _opposite_light_direction);
    _v0158 = vec3( 0.00000000E+00, 0.00000000E+00, -5.00000000E+00) - gl_TexCoord[3].xyz;
    _TMP13 = dot(_v0158, _v0158);
    _TMP14 = inversesqrt(_TMP13);
    _surface_to_camera_vector21 = _TMP14*_v0158;
    _v0164 = (2.00000000E+00*_diffuse)*_surface_normal - _opposite_light_direction;
    _TMP13 = dot(_v0164, _v0164);
    _TMP14 = inversesqrt(_TMP13);
    _reflection_vector = _TMP14*_v0164;
    _TMP9 = dot(_reflection_vector, _surface_to_camera_vector21);
    _TMP15 = min(1.00000000E+00, _TMP9);
    _TMP173 = max(0.00000000E+00, _TMP15);
    _TMP10 = min(cameraposition.z, 5.00000000E+02);
    _z_factor1 = (5.00000000E+02 - _TMP10)/5.00000000E+02;
    _TMP11 = min(gl_TexCoord[3].y, 3.50000000E+02);
    _y_factor1 = (3.50000000E+02 - _TMP11)/3.50000000E+02;
    _output_color.xyz = _output_color.xyz + _TMP173*_z_factor1*_y_factor1;
    _output_color.xyz = _output_color.xyz + reflectionparameters.z*_reflection_texel.xyz;
    _output_color.xyz = _output_color.xyz + gl_TexCoord[4].z*(fogcolor.xyz - _output_color.xyz);
    _TMP12 = texture2D(wateralphatexture, gl_TexCoord[5].xy);
    _output_color.w = 1.00000000E+00 - _TMP12.x;
    _o_color1 = _output_color;
    gl_FragColor = _output_color;
} // main end
