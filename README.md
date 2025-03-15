# README

上手机器学习想做点实验验证思路，但市面上都是小时计费的 GPU 服务器还要你配置 Docker？😡 这不是良好的体验。良好开发者体验：很多时候要一个极强的 GPU，跑十几分钟的小实验。但！一个弱的显卡（3090）很多想法是没法测。如果有这样一个平台，让你快速启动一个服务器，并且用上 H100？H200？是不是很爽？

👉 https://modal.com/ 一个 GPU Serverless 平台，每月送 30 USD Credit = 16 小时的 H200 或者 50 小时的 T4。

很适合大模型训练营的工程师来用。

👉 https://github.com/ipruning/run-your-py-on-serverless-gpu 为大家准备好的脚本，我因为个人偏好会选择 https://docs.marimo.io/ 来做交互式开发。

如果大家想用 jupyter 逻辑也是类似，略微修改即可。

```bash
./modal.bash notebook.py
```

## ChangeLog

- 250316 init
