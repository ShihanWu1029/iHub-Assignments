import moderngl
import numpy as np
import pygame
from pyrr import Matrix44

def main():
    # 初始化Pygame
    pygame.init()
    pygame.display.set_caption("带白色光源的立方体")
    
    # 配置OpenGL上下文，兼容Mac系统
    try:
        # 设置OpenGL 3.3核心模式
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, 
            pygame.GL_CONTEXT_PROFILE_CORE
        )
        screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
    except:
        # 兼容模式 fallback
        print("切换到兼容模式")
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 2)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, 
            pygame.GL_CONTEXT_PROFILE_COMPATIBILITY
        )
        screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)

    # 创建ModernGL上下文
    ctx = moderngl.create_context()
    #print(f"使用的OpenGL版本: {ctx.version}")
    
    # 启用深度测试
    ctx.enable(moderngl.DEPTH_TEST)

    # 顶点着色器
    vertex_shader = """
    #version 330 core
    
    in vec3 in_position;
    in vec3 in_normal;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    uniform vec3 light_pos;

    out vec3 v_normal;
    out vec3 v_light_dir;
    out vec3 v_frag_pos;

    void main() {
        gl_Position = projection * view * model * vec4(in_position, 1.0);
        v_frag_pos = vec3(model * vec4(in_position, 1.0));
        v_light_dir = light_pos - v_frag_pos;
        v_normal = mat3(transpose(inverse(model))) * in_normal;
    }
    """

    # 片段着色器 - 白色光源
    fragment_shader = """
    #version 330 core
    
    in vec3 v_normal;
    in vec3 v_light_dir;
    in vec3 v_frag_pos;

    uniform vec3 object_color;
    uniform vec3 light_color;  // 白色光源
    uniform vec3 light_pos;

    out vec4 frag_color;

    void main() {
        // 环境光
        float ambient_strength = 0.2;
        vec3 ambient = ambient_strength * light_color;
        
        // 漫反射光
        vec3 normal = normalize(v_normal);
        vec3 light_dir = normalize(v_light_dir);
        float diff = max(dot(normal, light_dir), 0.0);
        vec3 diffuse = diff * light_color;
        
        // 镜面反射光
        float specular_strength = 0.8;
        vec3 view_dir = normalize(vec3(0.0, 0.0, 5.0) - v_frag_pos);
        vec3 reflect_dir = reflect(-light_dir, normal);
        float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
        vec3 specular = specular_strength * spec * light_color;
        
        // 最终颜色
        vec3 result = (ambient + diffuse + specular) * object_color;
        frag_color = vec4(result, 1.0);
    }
    """

    # 创建着色器程序
    prog = ctx.program(
        vertex_shader=vertex_shader,
        fragment_shader=fragment_shader
    )

    # 立方体顶点数据 (位置和法向量)
    vertices = np.array([
        # 前面
        [-0.5, -0.5,  0.5,  0.0,  0.0,  1.0],
        [ 0.5, -0.5,  0.5,  0.0,  0.0,  1.0],
        [ 0.5,  0.5,  0.5,  0.0,  0.0,  1.0],
        [-0.5,  0.5,  0.5,  0.0,  0.0,  1.0],
        # 后面
        [-0.5, -0.5, -0.5,  0.0,  0.0, -1.0],
        [-0.5,  0.5, -0.5,  0.0,  0.0, -1.0],
        [ 0.5,  0.5, -0.5,  0.0,  0.0, -1.0],
        [ 0.5, -0.5, -0.5,  0.0,  0.0, -1.0],
        # 顶面
        [-0.5,  0.5, -0.5,  0.0,  1.0,  0.0],
        [-0.5,  0.5,  0.5,  0.0,  1.0,  0.0],
        [ 0.5,  0.5,  0.5,  0.0,  1.0,  0.0],
        [ 0.5,  0.5, -0.5,  0.0,  1.0,  0.0],
        # 底面
        [-0.5, -0.5, -0.5,  0.0, -1.0,  0.0],
        [ 0.5, -0.5, -0.5,  0.0, -1.0,  0.0],
        [ 0.5, -0.5,  0.5,  0.0, -1.0,  0.0],
        [-0.5, -0.5,  0.5,  0.0, -1.0,  0.0],
        # 右面
        [ 0.5, -0.5, -0.5,  1.0,  0.0,  0.0],
        [ 0.5,  0.5, -0.5,  1.0,  0.0,  0.0],
        [ 0.5,  0.5,  0.5,  1.0,  0.0,  0.0],
        [ 0.5, -0.5,  0.5,  1.0,  0.0,  0.0],
        # 左面
        [-0.5, -0.5, -0.5, -1.0,  0.0,  0.0],
        [-0.5, -0.5,  0.5, -1.0,  0.0,  0.0],
        [-0.5,  0.5,  0.5, -1.0,  0.0,  0.0],
        [-0.5,  0.5, -0.5, -1.0,  0.0,  0.0],
    ], dtype='f4')

    # 索引数据 - 确保正确绘制三角形
    indices = np.array([
        0, 1, 2, 0, 2, 3,  # 前面
        4, 5, 6, 4, 6, 7,  # 后面
        8, 9, 10, 8, 10, 11,  # 顶面
        12, 13, 14, 12, 14, 15,  # 底面
        16, 17, 18, 16, 18, 19,  # 右面
        20, 21, 22, 20, 22, 23   # 左面
    ], dtype='i4')

    # 创建缓冲区
    vbo = ctx.buffer(vertices.tobytes())
    ibo = ctx.buffer(indices.tobytes())

    # 创建顶点数组对象
    vao = ctx.vertex_array(
        prog,
        [(vbo, '3f 3f', 'in_position', 'in_normal')],
        ibo
    )

    # 设置Uniform变量 - 白色光源
    prog['object_color'].value = (0.3, 0.6, 0.9)  # 蓝色立方体
    prog['light_color'].value = (1.0, 1.0, 1.0)   # 白色光源
    prog['light_pos'].value = (3.0, 2.0, 4.0)     # 光源位置

    # 投影矩阵
    projection = Matrix44.perspective_projection(
        fovy=45.0, 
        aspect=800/600, 
        near=0.1, 
        far=100.0
    )
    prog['projection'].write(projection.astype('f4').tobytes())

    # 视图矩阵 (相机位置)
    view = Matrix44.look_at(
        eye=(0.0, 0.0, 5.0),    # 相机位置
        target=(0.0, 0.0, 0.0), # 目标点
        up=(0.0, 1.0, 0.0)      # 上方向
    )
    prog['view'].write(view.astype('f4').tobytes())

    # 主循环
    clock = pygame.time.Clock()
    running = True
    rotation_x = 0
    rotation_y = 0

    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 清除缓冲区
        ctx.clear(0.1, 0.1, 0.1)  # 深灰色背景
        
        # 更新旋转角度
        rotation_x += 0.5
        rotation_y += 0.7
        
        # 模型矩阵 (包含旋转)
        model = Matrix44.from_eulers((
            np.radians(rotation_x),
            np.radians(rotation_y),
            0.0,
        ))
        prog['model'].write(model.astype('f4').tobytes())
        
        # 渲染立方体
        vao.render()
        
        # 刷新屏幕
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()