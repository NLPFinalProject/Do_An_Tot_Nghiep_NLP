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
      console.log(data);
      console.log('yeah yeah yeah');
      this.PushDataToDisplayData(data);
      this.displayData = [...this.newDataList];
    });
    this.getData();
  }
  gotoDetail() {
    console.log('begin');
    this.router.navigate(['daovan/' + this.userData], { replaceUrl: true });
    // this.fileService.getResult(this.userData).subscribe((data: any) => {
    //   console.log(data);
    //   console.log('win');
    //   console.log(this.userData);
    //   //this.router.navigate([],{'data':data})
    //   this.router.navigate(['daovan/' + this.userData], { replaceUrl: true, state: { data: data } });
    // });
  }
  PushDataToDisplayData(data: any) {
    this.flag = true;
    this.newDataList = [];
    console.log('now');
    console.log(data);
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
  sort(sort: { key: string; value: string }): void {
    console.log(sort);
    console.log('why am I here, just to suffer?');
    this.sortName = sort.key;
    this.sortValue = sort.value;
    this.search();
  }

  filter(listOfSearchName: string[], searchAddress: string): void {
    this.listOfSearchName = listOfSearchName;
    this.searchAddress = searchAddress;
    this.search();
  }

  search(): void {
    // filter data
    const filterFunc = (item: any) =>
      (this.searchAddress ? item.address.indexOf(this.searchAddress) !== -1 : true) &&
      (this.listOfSearchName.length
        ? this.listOfSearchName.some((name: string) => item.name.indexOf(name) !== -1)
        : true);
    const data = this.data.filter((item) => filterFunc(item));
    // sort data
    if (this.sortName && this.sortValue) {
      this.displayData = data.sort((a, b) =>
        this.sortValue === 'ascend'
          ? a[this.sortName] > b[this.sortName]
            ? 1
            : -1
          : b[this.sortName] > a[this.sortName]
          ? 1
          : -1
      );
    } else {
      this.displayData = data;
    }
  }

  /**
   * Upload file to server
   */
  upload = (file: any) => {
    console.log('welcome');
    console.log(file.name);
    console.log(file);
    /*setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công'
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);*/
    // tslint:disable-next-line:semicolon
    this.fileService.UploadFile(file);
  };
  /* uploadFile = ((file: NzUploadFile) => {
    console.log('welcome to upload');
    /*console.log(file.name);
    console.log(file);
    this.FileToUpload = file;
    this.invalid();
    console.log(this.isvalid);
    console.log(file);
    this.FileToUpload = file;
    /*setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công'
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);
    this.fileService.UploadFile(this.FileToUpload).subscribe(data => {
      console.log(data);
    });
    // tslint:disable-next-line:semicolon
  };*/
  uploadFile = (file: UploadFile) => {
    console.log('welcome to upload');
    console.log(file.name);
    console.log(file);
    this.FileToUpload = file.this.invalid();
    console.log(this.isvalid);

    setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công',
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);
    this.fileService.UploadFile(this.FileToUpload).subscribe((data) => {
      console.log(data);
    });
    // tslint:disable-next-line:semicolon
  };
  uploadFileList = () => {
    this.invalid();

    /*setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công'
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);*/
    this.fileService.UploadFileList(this.ListFileToUpload).subscribe((data) => {
      console.log(data);
    });

    // tslint:disable-next-line:semicolon
  };
  invalid() {
    if (this.FileToUpload != null && this.ListFileToUpload != null) this.isvalid = true;
    else this.isvalid = false;
  }
  /*handleChange(info: UploadChangeParam): void {
    this.uploadFileList(null);
    if (info.file.status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === 'done') {
      this.msg.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === 'error') {
      this.msg.error(`${info.file.name} file upload failed.`);
    }
  }*/
  handleChange(file: FileList): void {
    //this.FileToUpload=file.item(0);
    //this.uploadFile();
    this.ListFileToUpload = file;
    this.uploadFileList();
  }
  checkPlagism() {
    console.log('can go here');
    this.router.navigate(['checkresult/step/1'], { replaceUrl: true });
  }
}
