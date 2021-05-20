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
//var sampler2D tex_0_d :  : _tex_0_d1 : 19 : 1
//\--replaced with p3d_Texture0_d
//var sampler2D tex_0_n :  : _tex_0_n1 : 20 : 1
//\--replaced with p3d_Texture0_n
//var sampler2D tex_0_bb :  : _tex_0_bb1 : 21 : 1
//\--replaced with p3d_Texture0_bb
//var sampler2D tex_0_low2 :  : _tex_0_low21 : 22 : 1
//\--replaced with p3d_Texture0_low2
//var sampler2D k_watercolortexture :  : _k_watercolortexture1 : 23 : 1
//\--replaced with watercolortexture
//var sampler2D k_reflectiontexture :  : _k_reflectiontexture1 : 24 : 1
//\--replaced with reflectiontexture
//var sampler2D k_wateralphatexture :  : _k_wateralphatexture1 : 25 : 1
//\--replaced with wateralphatexture
//var float2 l_texcoord0 : $vin.TEXCOORD0 : TEX0 : 0 : 1
//var float4 l_texcoord1 : $vin.TEXCOORD1 : TEX1 : 1 : 1
//var float3 l_normal : $vin.TEXCOORD2 : TEX2 : 2 : 1
//var float3 l_surface_pos : $vin.TEXCOORD3 : TEX3 : 3 : 1
//var float3 l_interpolate : $vin.TEXCOORD4 : TEX4 : 4 : 1
//var float2 l_alpha_uv : $vin.TEXCOORD5 : TEX5 : 5 : 1
//var float4 o_color : $vout.COLOR : COL : 26 : 1

#version 120

vec4 _o_color1;
vec4 _TMP9;
float _TMP8;
float _TMP6;
float _TMP12;
float _TMP11;
float _TMP10;
vec4 _TMP2;
vec4 _TMP1;
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
uniform sampler2D p3d_Texture0_d;
uniform sampler2D p3d_Texture0_bb;
uniform sampler2D p3d_Texture0_low2;
uniform sampler2D watercolortexture;
uniform sampler2D reflectiontexture;
uniform sampler2D wateralphatexture;
vec2 _c0034;
vec2 _c0038;
vec2 _c0040;
vec3 _v0084;
vec3 _v0090;
vec3 _v0096;
vec3 _v0116;
float _TMP125;

 // main procedure, the original name was fshader
void main()
{

    float _diffuse;
    float _specular;
    vec3 _light_direction;
    vec3 _opposite_light_direction;
    vec3 _reflection_vector;
    vec4 _colormap_d;
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

    _c0034 = (gl_TexCoord[0].xy + uvanim.xy)*2.00000000E+00;
    _colormap_d = texture2D(p3d_Texture0_d, _c0034);
    _c0038 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP1 = texture2D(p3d_Texture0_bb, _c0038);
    _normalmap2 = _TMP1*2.00000000E+00 - 1.00000000E+00;
    _c0040 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP2 = texture2D(p3d_Texture0_low2, _c0040);
    _normalmap3 = _TMP2 - 1.00000000E+00;
    _base_water_color = texture2D(watercolortexture, gl_TexCoord[4].xy);
    _base_water_color.xyz = _base_water_color.xyz*watercolorfactor.xyz + watercoloradd.xyz;
    _water_color = _colormap_d*1.00000001E-01 + _base_water_color;
    _projection_uv1 = gl_TexCoord[1].xy/gl_TexCoord[1].w;
    _projection_uv1 = _projection_uv1 + (_normalmap3.xy - _normalmap3.yx)*reflectionparameters.xy;
    _reflection_texel = texture2D(reflectiontexture, _projection_uv1);
    _camera_position.x = 0.00000000E+00;
    _camera_position.y = 0.00000000E+00;
    _camera_position.z = cameraposition.z;
    _v0084 = _camera_position.xyz - gl_TexCoord[3].xyz;
    _TMP10 = dot(_v0084, _v0084);
    _TMP11 = inversesqrt(_TMP10);
    _surface_to_camera_vector = _TMP11*_v0084;
    _v0090 = gl_TexCoord[3].xyz - lightposition.xyz;
    _TMP10 = dot(_v0090, _v0090);
    _TMP11 = inversesqrt(_TMP10);
    _light_direction = _TMP11*_v0090;
    _v0096 = -_light_direction;
    _TMP10 = dot(_v0096, _v0096);
    _TMP11 = inversesqrt(_TMP10);
    _opposite_light_direction = _TMP11*_v0096;
    _TMP10 = dot(vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00), vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00));
    _TMP11 = inversesqrt(_TMP10);
    _surface_normal = _TMP11*vec3( 0.00000000E+00, -1.00000001E-01, 1.00000000E+00);
    _surface_normal = _surface_normal + gl_TexCoord[2].xyz*1.00000001E-01 + _normalmap2.xyz*5.00000007E-02;
    _TMP10 = dot(_surface_normal, _surface_normal);
    _TMP11 = inversesqrt(_TMP10);
    _surface_normal = _TMP11*_surface_normal;
    _diffuse = dot(_surface_normal, _opposite_light_direction);
    _v0116 = (2.00000000E+00*_diffuse)*_surface_normal - _opposite_light_direction;
    _TMP10 = dot(_v0116, _v0116);
    _TMP11 = inversesqrt(_TMP10);
    _reflection_vector = _TMP11*_v0116;
    _TMP6 = dot(_reflection_vector, _surface_to_camera_vector);
    _TMP12 = min(1.00000000E+00, _TMP6);
    _TMP125 = max(0.00000000E+00, _TMP12);
    _TMP8 = pow(_TMP125, lightparameters.z);
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
    _output_color.xyz = _output_color.xyz + reflectionparameters.z*_reflection_texel.xyz;
    _output_color.xyz = _output_color.xyz + gl_TexCoord[4].z*(fogcolor.xyz - _output_color.xyz);
    _TMP9 = texture2D(wateralphatexture, gl_TexCoord[5].xy);
    _output_color.w = 1.00000000E+00 - _TMP9.x;
    _o_color1 = _output_color;
    gl_FragColor = _output_color;
} // main end
