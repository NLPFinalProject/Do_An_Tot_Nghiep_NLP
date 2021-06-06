import { Injectable } from '@angular/core';
import  {Subject} from 'rxjs'
@Injectable({
  providedIn: 'root'
})
export class DaovanServiceService {
  DisplayData1:Array<any>;
  DisplayData2:Array<any>;
  sendMessage = new Subject();
  sendMessageNumber = new Subject();
  public ChangeFile(filename:string)
  {
    
    this.sendMessage.next(filename)
  }
  public getSetting(pos:number)
  {
    this.sendMessageNumber.next(pos);
  }
  constructor() { }
}
