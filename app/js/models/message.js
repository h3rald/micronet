import { MicronetService } from '../services/micronet.svc.js';
import { Sensor } from '../models/sensor.js';

export class Message {

  constructor(obj) {
    this.api = new MicronetService();
    this.content = obj.payloadString;
    this.qos = obj.qos;
    this.retained = obj.retained;
    this.topic = obj.destinationName;
    this.topicParts = this.topic.split('/');
  }

  get device() {
    if (this.topicParts.length < 3) {
      return null;
    }
    return this.topicParts[2];
  }

  get type() {
    this.topicParts[3];
  }

  get sensor() {
    if (this.topicParts.length < 5) {
      return null;
    }
    var info = this.api.data.devices[this.device].info.sensors[this.topicParts[4]] || {};
    return new Sensor(info, this.value);
  }

  get value() {
    return JSON.parse(this.content);
  }
  

}
