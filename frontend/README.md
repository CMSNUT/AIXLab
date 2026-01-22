# frontend

## 项目结构

```sh
AIXLab/frontend
├─ docs                 # 项目文档工程
├─ public               # 静态资源文件
│  └─ docs              # 帮助文档模块
├─ src                  # 源代码
│  ├─ api               # 接口文件
│  ├─ assets            # 静态资源文件
│  ├─ components        # 组件模块
│  ├─ constants         # 常量模块
│  ├─ lang              # 语言模块
│  ├─ layouts           # 布局模块
│  ├─ plugins           # 插件模块
│  ├─ router            # 路由模块
│  ├─ store             # 状态管理模块
│  ├─ styles            # 样式模块
│  ├─ types             # 类型模块
│  ├─ utils             # 工具模块
│  ├─ view              # 视图模块
│  ├─ App.vue           # 根组件
│  ├─ main.js           # 入口文件
│  └─ settings.js       # 全局样式文件
├─ .env.dev             # 项目开发环境配置
├─ .env.prod            # 项目生产环境配置
├─ index.html           # 模板文件
├─ package.json         # 项目依赖文件
├─ tsconfig.json        # ts配置文件
├─ tsconfig.app.json    # 浏览器业务代码ts配置文件
├─ tsconfig.node.json   # node端ts配置文件
├─ uno.config.json      # uno配置文件
├─ vite.config.js       # vite服务配置文件
└─ README.md            # 项目说明文档

```

## 快速开始

```sh
# 进入前端工程目录
cd frontend
# 安装依赖
pnpm install
# 启动前端服务
pnpm run dev
# 构建前端, 生成 `frontend/dist` 目录
pnpm run build
# 运行命令，查看未用到的依赖
depcheck
```

# 手动安装依赖
```bash
pnpm add @element-plus/icons-vue @vue-flow/background @vue-flow/controls @vue-flow/core @vue-flow/minimap @vueuse/core @wangeditor-next/editor @wangeditor-next/editor-for-vue animate.css axios clipboard codemirror@^5 codemirror-editor-vue3 dayjs echarts element-plus exceljs file-saver highlight.js js-beautify markdown-it markdown-it-highlightjs nprogress path-browserify path-to-regexp pinia pinia-plugin-persistedstate qs vue vue-draggable-plus vue-i18n vue-json-pretty vue-router vue3-cron-plus vuedraggable
```

```bash
pnpm add -D @eslint/js @iconify/utils @types/codemirror @types/file-saver @types/markdown-it @types/node @types/nprogress @types/path-browserify @types/qs @typescript-eslint/eslint-plugin @typescript-eslint/parser @vitejs/plugin-vue autoprefixer commitizen cz-git eslint eslint-config-prettier eslint-plugin-prettier eslint-plugin-vue fs-extra globals husky lint-staged postcss postcss-html postcss-scss prettier sass stylelint stylelint-config-html stylelint-config-recess-order stylelint-config-recommended stylelint-config-recommended-scss stylelint-config-recommended-vue stylelint-prettier terser typescript typescript-eslint unocss unplugin-auto-import unplugin-vue-components vite vue-eslint-parser vue-tsc
```