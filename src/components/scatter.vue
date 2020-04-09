<script>
import { Scatter } from 'vue-chartjs/src/BaseCharts'
import { mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Scatter,
  name: 'scatter',
  mixins: [reactiveProp],
  props: ['chartData', 'options'],

  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
</script>
