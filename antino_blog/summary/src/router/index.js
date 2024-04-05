import { createRouter, createWebHistory } from 'vue-router'
import WeeklyChart from '@/components/WeeklyChart.vue'
import MonthlyChart from '@/components/MonthlyChart.vue'
import QuaterlyChart from '@/components/QuaterlyChart.vue'
import YearlyChart from '@/components/YearlyChart.vue'

const routes = [
  {
    path: '/weekly_report',
    name: 'weeklychart',
    component: WeeklyChart
  },
  {
    path: '/monthly_report',
    name: 'monthlychart',
    component: MonthlyChart
  },
  {
    path: '/quarterly_report',
    name: 'quaterlychart',
    component: QuaterlyChart
  },
  {
    path: '/yearly_report',
    name: 'yearlychart',
    component: YearlyChart
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
