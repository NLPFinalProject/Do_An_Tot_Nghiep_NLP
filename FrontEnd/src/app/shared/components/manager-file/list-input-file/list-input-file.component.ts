import { Component, OnInit, Input } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
import { UploadChangeParam, NzUploadModule, UploadFile, NzUploadComponent } from 'ng-zorro-antd/upload';
import { SessionToHistoryService } from '../../session-to-history.service';

import { NzMessageService } from 'ng-zorro-antd/message';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { RouterModule, Router } from '@angular/router';
@Component({
  selector: 'app-list-input-file',
  templateUrl: './list-input-file.component.html',
  styleUrls: ['./list-input-file.component.scss'],
})
export class ListInputFileComponent implements OnInit {
  // @Input() HisoryData:Array<any>;
  statusList = [
    { text: 'Chờ', value: 'Peding' },
    { text: 'Thành công', value: 'Sucess' },
    { text: 'Thất bại', value: 'Error' },
  ];
  isvalid: boolean = false;
  flag = false;
  msg: NzMessageService;
  userData: any = 0;
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  FileToUpload: File = null;
  ListFileToUpload: FileList = null;
  newDataList = Array<any>();
  data = Array<any>();

  fileList: Array<object> = [];
  constructor(
    private messageService: MessageService,
    private fileService: FileService,
    private router: Router,
    private sessionToHistory: SessionToHistoryService
  ) {}
  ngOnInit(): void {
    console.log('this is');
    this.fileService;
    this.sessionToHistory.sendListFile.subscribe((data: any) => {
      this.PushDataToDisplayData(data);
      this.displayData = [...this.newDataList];
    });
    this.getData();
  }

  PushDataToDisplayData(data: any) {
    this.flag = true;
    this.newDataList = [];

    for (var i = 0; i < data.filename.length; i++) {
      let temp = {
        name: data.filename[i],
        status: 'Thành công',
      };
      this.newDataList.push(temp);
    }
    this.userData = data.sessionId;
  }
  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData = [...this.data];
      this.loading = false;
    }, number);
  }

  checkPlagism() {
    this.router.navigate(['checkresult/step/1'], { replaceUrl: true });
  }

  /**
   * Upload file to server
   */
}
