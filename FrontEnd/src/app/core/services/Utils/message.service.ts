import { Injectable } from '@angular/core';
import { NzMessageService, UploadFile } from 'ng-zorro-antd';
import { Subject } from 'rxjs';

@Injectable()
export class MessageService {
  private loaderSubject = new Subject<any>();
  private alertState = this.loaderSubject.asObservable();
  constructor(private message: NzMessageService) {}

  success(description: string): void {
    this.message.create('success', description);
  }

  warning(description: string): void {
    this.message.create('warning', description);
  }

  error(description: string): void {
    this.message.create('error', description);
  }
}
