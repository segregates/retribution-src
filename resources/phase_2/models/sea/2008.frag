#version 12

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
uniform sampler2D Texture0_d;
uniform sampler2D Texture0_bb;
uniform sampler2D Texture0_low2;
uniform sampler2D watercolortexture;
uniform sampler2D reflectiontexture;
uniform sampler2D wateralphatexture;
uniform vec4 p3d_Color;
vec2 _c0034;
vec2 _c0038;
vec2 _c0040;
vec3 _v0084;
vec3 _v0090;
vec3 _v0096;
vec3 _v0116;
float _TMP125;

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
    vec4 _water_color;
    vec4 _reflection_texel;
    vec2 _projection_uv1;
    vec3 _surface_to_camera_vector;
    vec3 _camera_position;
    vec3 _surface_normal;
    vec4 _output_color;

    _c0034 = (gl_TexCoord[0].xy + uvanim.xy)*2.00000000E+00;
    _colormap_d = texture2D(Texture0_d, _c0034);
    _c0038 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP1 = texture2D(Texture0_bb, _c0038);
    _normalmap2 = _TMP1*2.00000000E+00 - 1.00000000E+00;
    _c0040 = gl_TexCoord[0].xy + uvanim.xy;
    _TMP2 = texture2D(Texture0_low2, _c0040);
    _normalmap3 = _TMP2 - 1.00000000E+00;
    _water_color = _colormap_d*1.00000001E-01 + p3d_Color;
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
    if (_diffuse < 0.00000000E+00) {
        _diffuse = 0.00000000E+00;
        _specular = 0.00000000E+00;
    }
    if (_reflection_texel.w > 0.00000000E+00) { // if begin
        _specular = 0.00000000E+00;
    }
    _output_color = ambientcolor*_water_color + (_diffuse*diffusecolor)*_water_color + _specular*specularcolor;
    _output_color.xyz = _output_color.xyz + reflectionparameters.z*_reflection_texel.xyz;
    _output_color.xyz = _output_color.xyz + gl_TexCoord[4].z*(fogcolor.xyz - _output_color.xyz);
    _TMP9 = texture2D(wateralphatexture, gl_TexCoord[5].xy);
    _output_color.w = 1.00000000E+00 - _TMP9.x;
    _o_color1 = _output_color;
    gl_FragColor = _output_color;
}