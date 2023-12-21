import Image from 'next/image'
import styles from './page.module.css'
import SchedulerApp from './components/SchedulerApp'

export default function Home() {
  return (
    <div className="app-container">
      <SchedulerApp/>
    </div>
  )
}
