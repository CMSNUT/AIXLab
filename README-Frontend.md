# 1. 创建项目

```bash
pnpm create vite frontend -- --template vue-ts

cd frontend
pnpm install

pnpm dev

pnpm build
```

# 2.安装项目生产依赖(dependencies)

```bash
pnpm add @element-plus/icons-vue @vue-flow/background @vue-flow/controls @vue-flow/core @vue-flow/minimap @vueuse/core @wangeditor-next/editor @wangeditor-next/editor-for-vue animate.css axios clipboard codemirror codemirror-editor-vue3 dayjs echarts element-plus exceljs file-saver highlight.js js-beautify markdown-it markdown-it-highlightjs nprogress path-browserify path-to-regexp pinia pinia-plugin-persistedstate qs vue vue-draggable-plus vue-i18n vue-json-pretty vue-router vue3-cron-plus vuedraggable
```

# 3.安装项目开发依赖(devDependencies)

```bash
pnpm add -D @eslint/js @iconify/utils @types/codemirror @types/file-saver @types/markdown-it @types/node @types/nprogress @types/path-browserify @types/qs @typescript-eslint/eslint-plugin @typescript-eslint/parser @vitejs/plugin-vue autoprefixer commitizen cz-git eslint eslint-config-prettier eslint-plugin-prettier eslint-plugin-vue fs-extra globals husky lint-staged postcss postcss-html postcss-scss prettier sass stylelint stylelint-config-html stylelint-config-recess-order stylelint-config-recommended stylelint-config-recommended-scss stylelint-config-recommended-vue stylelint-prettier terser typescript typescript-eslint unocss unplugin-auto-import unplugin-vue-components vite vue-eslint-parser vue-tsc
```

# 运行

```bash
pnpm dev
```
