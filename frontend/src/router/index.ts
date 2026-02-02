import type { App } from "vue";
import { createRouter, createWebHashHistory, RouteLocationNormalized, type RouteRecordRaw } from "vue-router";
export const Layout = () => import("@/layouts/index.vue");
/**
 * 静态路由
 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: "/redirect",
    meta: { hidden: true },
    component: Layout,
    children: [
      {
        path: "/redirect/:path(.*)",
        component: () => import("@/views/redirect/index.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    meta: { hidden: true },
    component: () => import("@/views/module_system/auth/index.vue"),
  },
  {
    path: "/401",
    name: "401",
    meta: { hidden: true, title: "401" },
    component: () => import("@/views/error/401.vue"),
  },
  {
    path: "/404",
    name: "404",
    meta: { hidden: true, title: "404" },
    component: () => import("@/views/error/404.vue"),
  },
  {
    path: "/500",
    name: "500",
    meta: { hidden: true, title: "500" },
    component: () => import("@/views/error/500.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    component: () => import("@/views/error/404.vue"),
    meta: { hidden: true, title: "404" },
  },
  // 以下内容必须放在后面
  {
    path: "/",
    name: "/",
    redirect: "/home",
    component: Layout,
    children: [
      {
        path: "home",
        component: () => import("@/views/dashboard/index.vue"),
        // 用于 keep-alive 功能，需要与 SFC 中自动推导或显式声明的组件名称一致
        // 参考文档: https://cn.vuejs.org/guide/built-ins/keep-alive.html#include-exclude
        name: "Home",
        meta: {
          title: "首页",
          icon: "homepage",
          affix: true,
          keepAlive: true,
        },
      },
      {
        path: "profile",
        name: "Profile",
        meta: { title: "个人中心", icon: "user", hidden: true },
        component: () => import("@/views/current/profile.vue"),
      },
      // 应用内部打开页面
      {
        path: "internal-app/:appId",
        name: "InternalApp",
        meta: { title: "内部应用", icon: "Monitor", hidden: true, keepAlive: false },
        component: () => import("@/views/module_application/myapp/components/InternalApp.vue"),
      },
    ],
  },
  // {
  //   path: "/plot/basic",
  //   name: "BasicPlot",
  //   component: () => import("@/views/module_plot/basic_plot/index.vue"), // 你的列表页路径
  //   meta: { title: "基础绘图" }
  // },
  // // 新增：详情页路由（带动态id参数）
  // {
  //   path: "/plot/basic/:id",
  //   name: "BasicPlotDetail",
  //   component: () => import("@/views/module_plot/basic_plot/detail.vue"), // 你的详情页路径
  //   meta: { title: "基础绘图模块" },
  //   props: true // 支持路由参数注入（可选，详情页已通过useRoute获取参数）
  // },

  // 动态路由（适合模块数量不固定，推荐）
  // {
  //   path: "/plot/:cate/index", 
  //   component: async (route) => {
  //     // 动态加载对应 code 的 index.vue
  //     const cate = route.params.cate as string;
  //     try {
  //       return await import(`@/views/module_plot/${cate}/index.vue`);
  //     } catch {
  //       return await import("@/views/error/404.vue");
  //     }
  //   },
  // },

  {
    path: "/plot/:category/:code",
    name: "PlotModule",  // 确保这个 name 存在
    meta: {
      title: "绘图模块",
      affix: false,
      keepAlive: true,
    },
    // component: () => import("@/views/module_plot/${category}/PlotModule.vue")
    component: () => import("@/views/module_plot/ModuleContainer.vue")
  }

    
];

/**
 * 创建路由
 */
const router = createRouter({
  history: createWebHashHistory(),
  routes: constantRoutes,
  // 刷新时，滚动条位置还原
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

// 全局注册 router
// 为了捕获并处理全局错误，在注册路由时添加错误处理
export function setupRouter(app: App<Element>) {
  app.use(router);
}

export default router;
