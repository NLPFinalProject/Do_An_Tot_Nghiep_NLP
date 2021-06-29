import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
@Injectable({
  providedIn: 'root',
})
export class SessionToHistoryService {
  DisplayData1: Array<any>;
  DisplayData2: Array<any>;

  sendListFile = new Subject();

  public sendFileList(filelist: any) {
    this.sendListFile.next(filelist);
  }
  constructor() {}
}
