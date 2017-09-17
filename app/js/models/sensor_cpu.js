import { Sensor } from './sensor.js';

export class CpuSensor extends Sensor {

  constructor(obj, value) {
    super(obj, value);
    this.cores = obj.cores;
    this.frequency = obj.frequency;
  }
}
