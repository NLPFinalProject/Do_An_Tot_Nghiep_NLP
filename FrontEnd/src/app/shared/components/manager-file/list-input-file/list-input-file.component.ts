import { Component, OnInit } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';

@Component({
  selector: 'app-list-input-file',
  templateUrl: './list-input-file.component.html',
  styleUrls: ['./list-input-file.component.scss']
})
export class ListInputFileComponent implements OnInit {
  statusList = [
    { text: 'Chờ', value: 'Peding' },
    { text: 'Thành công', value: 'Sucess' },
    { text: 'Thất bại', value: 'Error' }
  ];
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  data = [
    {
      name: 'Hoàn thiện các giải pháp QLNN đối với các hoạt động tôn giáo ở Việt Nam trong thời kỳ đổi mới.docx',
      status: 'Thất bại'
    },
    {
      name: 'Quản lý nhà nước đối với tập đoàn kinh tế tư nhân ở Việt Nam hiện nay.pdf',
      status: 'Chờ'
    },
    {
      name: 'Quản lý nhà nước về văn thư, lưu trữ.docx',
      status: 'Thất bại'
    },
    {
      name: 'Quản lý nhà nước về quy hoạch xây dựng nông thôn mới.docx',
      status: 'Thành công'
    }
  ];
  fileList: Array<object> = [];
  constructor(private messageService: MessageService) {}
  ngOnInit(): void {
    this.getData();
  }

  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData = [...this.data];
      this.loading = false;
    }, number);
  }
  sort(sort: { key: string; value: string }): void {
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
    const data = this.data.filter(item => filterFunc(item));
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
    setTimeout(() => {
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
    // tslint:disable-next-line:semicolon
  };
}
