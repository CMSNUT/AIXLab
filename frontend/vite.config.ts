// 核心：导入 Vue 编译插件，支持 .vue 文件解析
import vue from "@vitejs/plugin-vue";

// Vite 类型 + 工具函数：
// ConfigEnv：约束配置环境的类型（如 mode 字段）
// UserConfig：约束 Vite 配置对象的类型（TS 类型提示）
// loadEnv：加载 .env 环境变量文件（如 .env.dev）
// defineConfig：Vite 配置定义函数（提供类型提示 + 支持函数式配置）
import { type ConfigEnv, type UserConfig, loadEnv, defineConfig } from "vite";

// 自动导入插件：
// AutoImport：自动导入 Vue/Element Plus 等的 API（如 ref、ElMessage）
// Components：自动导入 Vue 组件（无需手动注册）
// ElementPlusResolver：Element Plus 自动导入解析器（识别组件/API）
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";

// UnoCSS Vite 插件（集成原子化 CSS）
import UnoCSS from "unocss/vite";

// Node.js 路径工具：解析绝对路径（避免相对路径混乱）
import { resolve } from "path";

// 导入 package.json 信息：用于构建全局 APP_INFO 变量
import { name, version, engines, dependencies, devDependencies } from "./package.json";

// 定义全局 APP_INFO 变量（前端代码可直接访问 __APP_INFO__）
// 包含包信息 + 构建时间，提供 TS 类型提示
// 平台的名称、版本、运行所需的 node 版本、依赖、构建时间的类型提示
const __APP_INFO__ = {
  pkg: { name, version, engines, dependencies, devDependencies },
  buildTimestamp: Date.now(),
};

// 解析 src 目录的绝对路径（统一路径别名 @ 的指向）
const pathSrc = resolve(__dirname, "src");

// 函数式配置：接收环境参数（mode），返回 Vite 配置对象
// Vite配置  https://cn.vitejs.dev/config
export default defineConfig(({ mode }: ConfigEnv): UserConfig => {
  // 加载对应环境的 .env 文件：
  // mode = development → 加载 .env.development
  // process.cwd()：项目根目录（确保加载正确的 .env 文件）
  const env = loadEnv(mode, process.cwd());

  // 判断是否为生产环境（用于区分构建/开发配置）
  const isProduction = mode === "production";

  return {
    // 部署基础路径：项目打包后部署在域名的 / 子路径下（如 https://xxx.com/）
    base: "/",

    // 路径解析配置
    resolve: {
      // 路径别名：@ 指向 src 目录（对应 TS 配置的 paths）
      alias: {
        "@": pathSrc,
      },
    },

    // CSS 预处理器配置
    css: {
      preprocessorOptions: {
        // 定义全局 SCSS 变量
        scss: {
          // api: "modern-compiler",
          // 全局注入 SCSS 变量：所有 SCSS 文件无需手动 import 就能用 variables.scss 的变量
          additionalData: `@use "@/styles/variables.scss" as *;`,
        },
      },
    },

    // 开发服务器配置
    server: {
      // 允许外部访问（等价于 0.0.0.0，局域网其他设备可访问）
      host: true,

      // 开发服务器端口：从环境变量读取，转为数字
      port: Number(env.VITE_APP_PORT),

      // 启动后自动打开浏览器
      open: true,

      // 接口代理（解决跨域问题）
      proxy: {
        // 代理 /dev-api 的请求
        [env.VITE_APP_BASE_API]: {
          // 后端接口目标地址：从环境变量读取（如 https://api.xxx.com）
          target: env.VITE_API_BASE_URL, // 代理目标地址：https://后端地址

          // 不验证 HTTPS 证书（适配后端自签证书场景）
          secure: false, // 请求是否https

          // 开启跨域（修改请求头的 Origin 为目标地址）
          changeOrigin: true, // 是否跨域
          // 注释掉的路径重写：原本用于移除代理前缀（如 /dev-api/user → /user）
          // rewrite: (path: string) => path.replace(new RegExp("^" + env.VITE_APP_BASE_API), ""),
        },
      },
    },

    // 插件列表（核心功能扩展）
    plugins: [
      // 启用 Vue 编译插件（必选）
      vue(),

      // 启用 UnoCSS（原子化 CSS）
      UnoCSS(),

      // 自动导入 API 插件配置
      // API 自动导入
      AutoImport({
        // 自动导入这些库的 API（无需手动 import）：
        // Vue（ref/reactive）、VueUse（useStorage）、Pinia（defineStore）、Vue Router、Vue I18n
        // 导入 Vue 函数，如：ref, reactive, toRef 等
        imports: ["vue", "@vueuse/core", "pinia", "vue-router", "vue-i18n"],

        resolvers: [
          // 导入 Element Plus函数，如：ElMessage, ElMessageBox 等
          // 自动导入 Element Plus 的 API（如 ElMessage、ElMessageBox）
          // importStyle: "sass"：导入 Sass 样式（支持主题定制）
          ElementPlusResolver({ importStyle: "sass" }),
        ],
        eslintrc: {
          // 关闭自动生成 ESLint 配置文件（避免覆盖现有配置）
          enabled: false,
          // 生成的 ESLint 配置路径（enabled: false 时无效，冗余配置）
          filepath: "./.eslintrc-auto-import.json",
          // 全局变量属性值（enabled: false 时无效，冗余配置）
          globalsPropValue: true,
        },

        // 支持在 Vue 模板中自动导入 API（如模板中用 ref 无需 import）
        vueTemplate: true,
        // 生成自动导入的 TS 类型声明文件（让 TS 识别全局 API）
        // 导入函数类型声明文件路径 (false:关闭自动生成)
        dts: "src/types/auto-imports.d.ts",
      }),
      // 组件自动导入
      Components({
        resolvers: [
          // 导入 Element Plus 组件
          ElementPlusResolver({ importStyle: "sass" }),
        ],
        // 指定自定义组件位置(默认:src/components)
        dirs: ["src/components", "src/**/components"],
        // 导入组件类型声明文件路径 (false:关闭自动生成)
        dts: "src/types/components.d.ts",
      }),
    ],
    // 预加载项目必需的组件
    optimizeDeps: {
      include: [
        "vue",
        "vue-router",
        "element-plus",
        "pinia",
        "axios",
        "@vueuse/core",
        "@wangeditor-next/editor-for-vue",
        "codemirror-editor-vue3",
        "default-passive-events",
        "exceljs",
        "path-to-regexp",
        "echarts/core",
        "echarts/renderers",
        "echarts/charts",
        "echarts/components",
        "vue-i18n",
        "nprogress",
        "qs",
        "path-browserify",
        "@element-plus/icons-vue",
        "element-plus/es",
        "element-plus/es/locale/lang/en",
        "element-plus/es/locale/lang/zh-cn",
        "element-plus/es/components/alert/style/index",
        "element-plus/es/components/avatar/style/index",
        "element-plus/es/components/backtop/style/index",
        "element-plus/es/components/badge/style/index",
        "element-plus/es/components/base/style/index",
        "element-plus/es/components/breadcrumb-item/style/index",
        "element-plus/es/components/breadcrumb/style/index",
        "element-plus/es/components/button/style/index",
        "element-plus/es/components/card/style/index",
        "element-plus/es/components/cascader/style/index",
        "element-plus/es/components/checkbox-group/style/index",
        "element-plus/es/components/checkbox/style/index",
        "element-plus/es/components/col/style/index",
        "element-plus/es/components/color-picker/style/index",
        "element-plus/es/components/config-provider/style/index",
        "element-plus/es/components/date-picker/style/index",
        "element-plus/es/components/descriptions-item/style/index",
        "element-plus/es/components/descriptions/style/index",
        "element-plus/es/components/dialog/style/index",
        "element-plus/es/components/divider/style/index",
        "element-plus/es/components/drawer/style/index",
        "element-plus/es/components/dropdown-item/style/index",
        "element-plus/es/components/dropdown-menu/style/index",
        "element-plus/es/components/dropdown/style/index",
        "element-plus/es/components/empty/style/index",
        "element-plus/es/components/form-item/style/index",
        "element-plus/es/components/form/style/index",
        "element-plus/es/components/icon/style/index",
        "element-plus/es/components/image-viewer/style/index",
        "element-plus/es/components/image/style/index",
        "element-plus/es/components/input-number/style/index",
        "element-plus/es/components/input-tag/style/index",
        "element-plus/es/components/input/style/index",
        "element-plus/es/components/link/style/index",
        "element-plus/es/components/loading/style/index",
        "element-plus/es/components/menu-item/style/index",
        "element-plus/es/components/menu/style/index",
        "element-plus/es/components/message-box/style/index",
        "element-plus/es/components/message/style/index",
        "element-plus/es/components/notification/style/index",
        "element-plus/es/components/option/style/index",
        "element-plus/es/components/pagination/style/index",
        "element-plus/es/components/popover/style/index",
        "element-plus/es/components/progress/style/index",
        "element-plus/es/components/radio-button/style/index",
        "element-plus/es/components/radio-group/style/index",
        "element-plus/es/components/radio/style/index",
        "element-plus/es/components/row/style/index",
        "element-plus/es/components/scrollbar/style/index",
        "element-plus/es/components/select/style/index",
        "element-plus/es/components/skeleton-item/style/index",
        "element-plus/es/components/skeleton/style/index",
        "element-plus/es/components/step/style/index",
        "element-plus/es/components/steps/style/index",
        "element-plus/es/components/sub-menu/style/index",
        "element-plus/es/components/switch/style/index",
        "element-plus/es/components/tab-pane/style/index",
        "element-plus/es/components/table-column/style/index",
        "element-plus/es/components/table/style/index",
        "element-plus/es/components/tabs/style/index",
        "element-plus/es/components/tag/style/index",
        "element-plus/es/components/text/style/index",
        "element-plus/es/components/time-picker/style/index",
        "element-plus/es/components/time-select/style/index",
        "element-plus/es/components/timeline-item/style/index",
        "element-plus/es/components/timeline/style/index",
        "element-plus/es/components/tooltip/style/index",
        "element-plus/es/components/tree-select/style/index",
        "element-plus/es/components/tree/style/index",
        "element-plus/es/components/upload/style/index",
        "element-plus/es/components/watermark/style/index",
        "element-plus/es/components/tour/style/index",
        "element-plus/es/components/tour-step/style/index",
        "element-plus/es/components/popconfirm/style/index",
        "element-plus/es/components/container/style/index",
        "element-plus/es/components/main/style/index",
        "element-plus/es/components/aside/style/index",
        "element-plus/es/components/footer/style/index",
        "element-plus/es/components/header/style/index",
        "element-plus/es/components/slider/style/index",
        "element-plus/es/components/button-group/style/index",
        "element-plus/es/components/result/style/index",
        "element-plus/es/components/checkbox-button/style/index",
        "element-plus/es/components/space/style/index",
      ],
    },
    // 构建配置
    build: {
      chunkSizeWarningLimit: 4000, // 消除打包大小超过4000kb警告
      minify: isProduction ? "terser" : false, // 只在生产环境启用压缩
      terserOptions: isProduction
        ? {
            compress: {
              keep_infinity: true, // 防止 Infinity 被压缩成 1/0，这可能会导致 Chrome 上的性能问题
              drop_console: true, // 生产环境去除 console.log, console.warn, console.error 等
              drop_debugger: true, // 生产环境去除 debugger
              pure_funcs: ["console.log", "console.info"], // 移除指定的函数调用
            },
            format: {
              comments: true, // 保留注释
            },
          }
        : {},
      rollupOptions: {
        output: {
          // manualChunks: {
          //   "vue-i18n": ["vue-i18n"],
          // },
          manualChunks(id) {
            if (id.includes("node_modules")) {
              // 针对大型库进行单独拆分
              if (id.includes("echarts")) {
                return "echarts";
              }
              if (id.includes("element-plus")) {
                return "element-plus";
              }
              if (id.includes("@wangeditor-next")) {
                return "wangeditor";
              }
              if (id.includes("codemirror")) {
                return "codemirror";
              }
              if (id.includes("exceljs")) {
                return "exceljs";
              }

              // 其他模块保持当前拆分方式
              const module = id.toString().split("node_modules/")[1].split("/")[0];
              if (["birpc", "hookable"].includes(module)) return;
              return module;
            }
          },
          // 用于从入口点创建的块的打包输出格式[name]表示文件名,[hash]表示该文件内容hash值
          entryFileNames: "js/[name].[hash].js",
          // 用于命名代码拆分时创建的共享块的输出命名
          chunkFileNames: "js/[name].[hash].js",
          // 用于输出静态资源的命名，[ext]表示文件扩展名
          assetFileNames: (assetInfo: any) => {
            const info = assetInfo.name.split(".");
            let extType = info[info.length - 1];
            // console.log('文件信息', assetInfo.name)
            if (/\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/i.test(assetInfo.name)) {
              extType = "media";
            } else if (/\.(png|jpe?g|gif|svg)(\?.*)?$/.test(assetInfo.name)) {
              extType = "img";
            } else if (/\.(woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name)) {
              extType = "fonts";
            }
            return `${extType}/[name].[hash].[ext]`;
          },
        },
      },
    },
    define: {
      __APP_INFO__: JSON.stringify(__APP_INFO__),
    },
  };
});

