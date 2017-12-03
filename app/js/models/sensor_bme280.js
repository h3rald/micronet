import { Sensor } from './sensor.js';

export class Bme280Sensor extends Sensor {

  constructor(obj, value) {
    super(obj, value);
  }

  get temperature() {
    return this.value[0];
  }

  get pressure() {
    return this.value[1];
  }

  get humidity() {
    return this.value[2];
  }

}
