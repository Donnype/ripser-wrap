<template>
    <div class="home">
        <div class="card" style="background-color: #2c3e50; margin: 10px">
            <div class="card-body">
                <div class="row">
                    <div class="col-5">
                        <div class="custom-file" style="width: 80%">
                            <input type="file" ref="file" id="file" class="custom-file-input"
                                   v-on:change="handleFileUpload()">
                            <label class="custom-file-label" for="file">Choose CSV file</label>
                        </div>
                        <a tabindex="0" role="button" class="btn" data-toggle="popover" data-trigger="focus"
                           style="background-color: #6C747D; margin-left: 5px"
                           data-content="
                                The csv file must be of the form [ [-1, 1], [1, 1], ...].
                                The maximal dimension is 2 and the points must lie within [-1, 1] x [-1, 1]">
                            <i class="fa fa-question"></i>
                        </a>
                    </div>
                    <div class="col-2">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text">Prime</span>
                            </div>
                            <input v-model="prime" type="text" class="form-control">
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text">Maximal dimension:</span>
                            </div>
                            <div class="input-group-append">
                                <select v-model="maxDim" class="custom-select">
                                    <option v-bind:key="option" v-for="option in [0, 1]">{{ option }}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="col-2">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text">Compute cocycles:</span>
                            </div>
                            <div class="input-group-prepend">
                                <div class="input-group-text">
                                    <input v-model="do_cocycles" type="checkbox"
                                           aria-label="Checkbox for following text input">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row justify-content-between">
            <div class="col-6">
                <div class="card" style="background-color: #2c3e50; margin: 20px">
                    <div class="card-body">
                        <h3 class="card-title">Click to add data:
                            <a tabindex="0" role="button" class="btn" data-toggle="popover" data-trigger="focus"
                               style="background-color: #6C747D; margin-left: 5px"
                               data-content="Click in the area below to add points to analyze, or add the data in csv
                               format. After submitting the data, increase the threshold to reveal the cocycles.">
                                <i class="fa fa-question"></i>
                            </a>
                        </h3>
                        <Scatter id="userInput"
                                 style="background-color: #19222E"
                                 :chart-data=formattedHistory
                                 :options=fixedOptions
                        ></Scatter>
                        <button class="btn btn-primary" style="margin: 5px" @click="submitHistory">Submit</button>
                        <button class="btn btn-secondary" style="margin: 5px" @click="clearHistory">Clear</button>
                        <div>
                            Threshold:
                            <vue-slider v-model="threshold" v-bind="sliderOptions" ref="slider"/>
                            {{ threshold }}
                        </div>
                        <div v-if="cocycles1.length > 1">
                            {{ cocycles1.length }} cocycles in dimension 1 found, current: {{ selectedCocycle }}
                            <vue-slider
                                    v-model="selectedCocycle"
                                    v-bind="cocycleSliderOptions"
                                    :data="cocycleList"
                                    ref="slider2"/>
                        </div>
                        <div v-if="cocycles1.length === 1">
                            One cocycle in dimension 1 found.
                        </div>
                        <div v-if="labels.length > 0">
                            The image of the edges when the cocycle is viewed as a map from edges the integers:
                            <i v-bind:key="label" v-for="label in labels" style="margin-right: 10px">
                                <i class="fa fa-square fa-2x" v-bind:style="{'color': randomColors[label]}">
                                </i>: {{ label }}
                            </i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <div class="card" style="background-color: #2c3e50; margin: 20px">
                    <div class="card-body">
                        <h3 class="card-title">Persistence diagram dimension 1
                            <a tabindex="0" role="button" class="btn" data-toggle="popover" data-trigger="focus"
                               style="background-color: #6C747D; margin-left: 5px"
                               data-content="This diagram shows the life spans of the cocycles computed in dimension 1.
                               Once there are points in this chart after submitting the data, move the threshold
                               to see the selected cocycle in terms of the image of the edges in Z/pZ">
                                <i class="fa fa-question"></i>
                            </a>
                        </h3>
                        <Scatter :chart-data=data1 :options=options></Scatter>
                    </div>
                </div>
                <div class="card" style="background-color: #2c3e50; margin: 20px">
                    <div class="card-body">
                        <h3 class="card-title">Persistence diagram dimension 0
                            <a tabindex="0" role="button" class="btn" data-toggle="popover" data-trigger="focus"
                               style="background-color: #6C747D; margin-left: 5px"
                               data-content="This diagram shows the life span of what could be interpreted as
                               the connected components.">
                                <i class="fa fa-question"></i>
                            </a>
                        </h3>
                        <Scatter :chart-data=data0 :options=options></Scatter>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Scatter from '../../src/components/scatter'
import vueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import axios from 'axios'
import {randomColors} from '../variables'

export default {
  name: 'home',
  components: {
    Scatter,
    vueSlider
  },
  data () {
    return {
      prime: 31,
      maxDim: 1,
      threshold: 0,
      do_cocycles: true,
      randomColors: randomColors,
      labels: [],
      cocycles0: [],
      cocycles1: [],
      data0: [],
      data1: [],
      distanceMatrix: [],
      selectedCocycle: 0,
      history: [],
      formattedHistory: [],
      diagonalLineData: [],
      sliderOptions: {
        dotSize: 14,
        width: 'auto',
        height: 4,
        contained: false,
        direction: 'ltr',
        min: 0.0,
        max: 2.0,
        interval: 0.001,
        disabled: false,
        clickable: true,
        duration: 0.5,
        useKeyboard: true,
        dragOnClick: true
      },
      cocycleSliderOptions: {
        dotSize: 14,
        width: 'auto',
        height: 4,
        contained: false,
        direction: 'ltr',
        disabled: false,
        clickable: true,
        duration: 0.5,
        useKeyboard: true,
        dragOnClick: true
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          labels: {
            fontColor: 'whitesmoke'
          }
        },
        scales: {
          yAxes: [
            {
              ticks: {
                fontColor: '#728FA4'
              },
              gridLines: {
                color: '#4E667A'
              }
            }],
          xAxes: [
            {
              ticks: {
                fontColor: '#728FA4'
              },
              gridLines: {
                color: '#4E667A'
              }
            }]
        }
      },
      fixedOptions: {
        align: 'center',
        responsive: true,
        maintainAspectRatio: true,
        animation: {
          duration: 0
        },
        legend: {
          display: false
        },
        onClick: event => this.addPoint(this.toCoordinates(event)),
        scales: {
          yAxes: [{
            ticks: {
              display: false,
              min: -1,
              max: 1
            },
            gridLines: {
              display: false
            }
          }],
          xAxes: [
            {
              ticks: {
                display: false,
                min: -1,
                max: 1
              },
              gridLines: {
                display: false
              }
            }]
        }
      }
    }
  },

  computed: {
    cocycleList () {
      return Array.from({length: this.cocycles1.length}, (x, i) => i)
    }
  },

  mounted () {
    for (let step = 0; step < 100; step++) {
      this.diagonalLineData.push({x: step / 100, y: step / 100})
    }
  },

  methods: {
    submitHistory () {
      let data = {
        prime: this.prime,
        do_cocycles: this.do_cocycles,
        points: this.history
      }

      axios.post('/api/upload_data',
        data,
        {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        }
      ).then(response => {
        this.handleResponse(response)
      }).catch(function (error) {
        console.error('Upload failed!')
        console.error(error)
      })
    },

    toPersistenceChartData: function (data, dimension) {
      let formattedData = []

      for (let point of data) {
        formattedData.push({x: point[0], y: point[1]})
      }

      return {
        datasets: [{
          label: 'Persistence Diagram in dimension ' + dimension,
          fill: false,
          borderColor: '#f87979',
          backgroundColor: '#f87979',
          data: formattedData
        }, {
          label: 'Birth Line',
          fill: false,
          borderColor: '#000000',
          backgroundColor: '#000000',
          data: this.diagonalLineData,
          pointRadius: 1,
          pointHoverRadius: 1
        }]
      }
    },

    handleResponse (response) {
      console.log('Upload successful')

      let diagrams = JSON.parse(response.data.diagrams)
      let cocycles = JSON.parse(response.data.cocycles)
      this.distanceMatrix = JSON.parse(response.data.distance_matrix)

      let diagram0 = JSON.parse(diagrams[0])
      let diagram1 = JSON.parse(diagrams[1])

      this.data0 = this.toPersistenceChartData(diagram0, 0)
      this.data1 = this.toPersistenceChartData(diagram1, 1)
      this.cocycles0 = JSON.parse(cocycles[0])
      this.cocycles1 = JSON.parse(cocycles[1])
      this.cocycleSliderOptions.max = this.cocycles1.length

      let maxRow1 = diagram0.map(function (row) {
        return Math.max.apply(Math, row)
      })
      let max1 = Math.max.apply(null, maxRow1)
      let maxRow2 = diagram1.map(function (row) {
        return Math.max.apply(Math, row)
      })
      let max2 = Math.max.apply(null, maxRow2)

      this.sliderOptions.max = Math.round(1000 * Math.max(max1, max2) + 300) / 1000
    },

    handleFileUpload: function () {
      let file = this.$refs.file.files[0]
      let reader = new FileReader()

      reader.onload = e => {
        let csv = e.target.result
        csv = csv.split('\n')
        csv.pop()

        for (let row of csv) {
          let coordinates = row.split(',')

          if (coordinates.length > 2) {
            break
          }

          // eslint-disable-next-line no-undef
          coordinates = coordinates.map($.trim).map(parseFloat)
          this.addPoint(coordinates)
        }
      }

      reader.readAsText(file)
    },

    clearHistory () {
      this.history = []
      this.cocycles0 = []
      this.cocycles1 = []
      this.labels = []
      this.threshold = 0
      this.selectedCocycle = 0

      this.formattedHistory = {
        datasets: [{
          fill: false,
          borderColor: '#f87979',
          backgroundColor: '#f87979',
          data: []
        }]
      }
    },

    toCoordinates (event) {
      let el = document.getElementById('userInput')
      let rect = el.getBoundingClientRect()

      // Correct for the current scroll position, the offset of the imput area and the ratio of the client
      let x = (event.clientX - rect.x - 10) / (rect.width - 10)
      let y = 1 - (event.clientY - rect.y - 4) / (rect.height - 10)

      // Rescale the coordinates linearly from [0, 1] x [0, 1] to [-1, 1] x [-1, 1]
      let xMin = this.fixedOptions.scales.xAxes[0].ticks.min
      let yMin = this.fixedOptions.scales.yAxes[0].ticks.min
      let xFactor = this.fixedOptions.scales.xAxes[0].ticks.max - xMin
      let yFactor = this.fixedOptions.scales.yAxes[0].ticks.max - yMin

      return [xFactor * x + xMin, yFactor * y + yMin]
    },

    addPoint (coordinates) {
      let [x, y] = coordinates
      this.history.push([x, y])
      let formattedData = []

      for (let point of this.history) {
        formattedData.push({x: point[0], y: point[1]})
      }

      this.formattedHistory = {
        datasets: [{
          label: 'skip',
          fill: false,
          borderColor: '#f87979',
          backgroundColor: '#f87979',
          data: formattedData
        }]
      }
    },

    showCocycle (threshold) {
      let cocycle = this.cocycles1[this.selectedCocycle]
      let formattedData = []
      this.labels = []

      for (let point of this.history) {
        formattedData.push({x: point[0], y: point[1]})
      }

      let dataSets = [{
        fill: false,
        borderColor: '#f87979',
        backgroundColor: '#f87979',
        data: formattedData
      }]

      for (let i of Array.from({length: this.history.length}, (x, i) => i)) {
        for (let j of Array.from({length: this.history.length}, (x, j) => j).splice(i, this.history.length)) {
          let distance = this.distanceMatrix[i][j]
          let cocycleValue = 0

          if (distance <= threshold) {
            for (let image of cocycle) {
              let [x, y, value] = image

              if ((x === i && y === j) || (x === j && y === i)) {
                cocycleValue = value
              }
            }

            if (!this.labels.includes(cocycleValue)) {
              this.labels.push(cocycleValue)
            }

            dataSets.push(
              {
                fill: false,
                showLine: true,
                borderWidth: 2,
                borderColor: randomColors[cocycleValue],
                backgroundColor: randomColors[cocycleValue],
                data: [
                  {x: this.history[i][0], y: this.history[i][1]},
                  {x: this.history[j][0], y: this.history[j][1]}
                ],
                legend: {
                  display: true
                }
              }
            )
          }
        }
      }

      this.formattedHistory = {
        datasets: dataSets
      }
    }
  },

  watch: {
    threshold: function (val) {
      if (this.cocycles1.length !== 0 && this.history.length !== 0) {
        this.showCocycle(val)
      }
    },

    selectedCocycle: function () {
      if (this.cocycles1.length !== 0) {
        this.showCocycle(this.threshold)
      }
    }
  }
}
</script>
