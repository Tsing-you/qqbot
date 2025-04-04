## NcatBot LLM 插件

### 介绍

LLM 插件不直接提供大语言模型对话服务, 而是提供基于事件的对话接口和基本配置服务.

### 配置项

使用 NcatBot 的内置配置项功能, 三个核心配置项如下:

- api: `/cfg LLM_API.api <your api>` api-key。
- url: `/cfg LLM_API.url <your url>` 基准 url。
- model: `/cfg LLM_API.model <your model>` 模型名。

例如 [Kimi](https://platform.moonshot.cn/docs/guide/migrating-from-openai-to-kimi#%E5%85%B3%E4%BA%8E-api-%E5%85%BC%E5%AE%B9%E6%80%A7):

```
url: https://api.moonshot.cn/v1
model: moonshot-v1-8k
api: <KEY>
```

### 事件

通过 `LLM_API.main` 事件触发调用 LLM 的服务, 事件参数的 data 部分为 LLM 输入参数, 事件的处理结果为 LLM 的回复.

`data` 的构造如下:

```
{
    "history": [
        {
            "role": "system",
            "content": "系统提示内容"
        },
        {
            "role": "user",
            "content": "用户输入内容"
        },
    ], # 提示信息
    "max_tokens": 4096, # 最大长度
    "temperature": 0.7 # 温度,
}
```

`result` 的构造如下:

```
{
    "text": "回复内容",
    "status": "状态码" # 200 表示成功, 其他表示失败
    "error": "错误信息" # 
}
```

### 测试

管理员权限可以使用 `/tllma` 触发测试事件.