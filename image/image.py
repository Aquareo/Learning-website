import base64
from PIL import Image
import io
import os

def base64_to_image(base64_str, output_path="output.png"):
    """将base64字符串转换为图片"""
    try:
        # 检查并处理base64字符串
        base64_str = base64_str.strip()
        # 补充=号使其成为4的倍数
        if len(base64_str) % 4 != 0:
            base64_str += "=" * (4 - len(base64_str) % 4)
            
        # 解码base64数据
        image_data = base64.b64decode(base64_str)
        
        # 使用PIL打开图片数据
        with io.BytesIO(image_data) as bio:
            image = Image.open(bio)
            # 强制加载图片数据
            image.load()
            # 保存图片
            image.save(output_path)
            print(f"图片已成功保存至: {output_path}")
            return True
            
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False

def image_to_base64(image_path):
    """将图片转换为base64字符串"""
    try:
        with open(image_path, "rb") as image_file:
            # 读取并编码图片数据
            base64_data = base64.b64encode(image_file.read())
            return base64_data.decode()
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return None

def read_base64_from_file(file_path):
    """从文件中读取base64字符串"""
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        print(f"读取文件失败: {str(e)}")
        return None

if __name__ == "__main__":
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建base64_data.txt的完整路径
    file_path = os.path.join(current_dir, 'base64_data.txt')
    
    print(f"正在读取文件: {file_path}")
    base64_str = read_base64_from_file(file_path)
    if base64_str:
        print(f"成功读取base64字符串,长度: {len(base64_str)}")
        base64_to_image(base64_str)
    else:
        print("读取base64字符串失败")