import type { App } from "vue";
import { createRouter, createWebHashHistory, type RouteRecordRaw } from "vue-router";
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


  //  下面是成功的，但没有了布局
  // {
  //   path: "/plot/:category/:code",
  //   name: "PlotModule",  // 确保这个 name 存在
  //   meta: {
  //     title: "绘图模块",
  //     affix: false,
  //     keepAlive: true,
  //   },
  //   // component: () => import("@/views/module_plot/${category}/PlotModule.vue")
  //   component: () => import("@/views/module_plot/ModuleContainer.vue")
  // }

  {
    path: '/plot', // 父路由路径
    redirect: "/plot/basic",
    // 内联组件：无需新建ParentPlot.vue，直接渲染router-view，避免路径错误
    component: Layout,
    // 子路由（必须嵌套在children数组中，路径不要加/）
    children: [
      {
        path: ':category/:code', // 子路由相对路径（不要写 /:category/:code）
        name: 'PlotModule', // 唯一名称，确保全局无重复
        meta:{
          title: '绘图模块',
          hidden: true, 
          keepAlive: true
        },
        component: () => import('@/views/module_plot/ModuleContainer.vue') // 确认这个文件存在
      }
    ]
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
