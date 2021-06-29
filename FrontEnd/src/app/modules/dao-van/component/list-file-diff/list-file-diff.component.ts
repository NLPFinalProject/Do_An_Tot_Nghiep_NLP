import { Component, OnInit, Input } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
import { DaovanServiceService } from '../../daovan-service.service';
@Component({
  selector: 'app-list-file-diff',
  templateUrl: './list-file-diff.component.html',
  styleUrls: ['./list-file-diff.component.scss'],
})
export class ListFileDiffComponent implements OnInit {
  @Input() FileList2: Array<any>;
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  data = [
    {
      name: 'Hoàn thiện các giải pháp QLNN đối với các hoạt động tôn giáo ở Việt Nam trong thời kỳ đổi mới.docx',
      count: 80,
    },
    {
      name: 'Quản lý nhà nước đối với tập đoàn kinh tế tư nhân ở Việt Nam hiện nay.pdf',
      count: 60,
    },
    {
      name: 'Quản lý nhà nước về văn thư, lưu trữ.docx',
      count: 40,
    },
    {
      name: 'Quản lý nhà nước về quy hoạch xây dựng nông thôn mới.docx',
      count: 6,
    },
  ];
  fileList: Array<object> = [];
  constructor(private messageService: MessageService, private DaoVanService: DaovanServiceService) {}
  ngOnInit(): void {
    this.getData();
  }
  ngOnChanges() {
    //this.childFunction()
    console.log('I have change');
    console.log(this.FileList2);
    this.getData();
  }
  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData = [...this.FileList2];
      this.loading = false;
    }, number);
  }
  sendMessage(name: string) {
    console.log('this is data', name);
    for (var i = 0; i < this.FileList2.length; i++) {
      console.log('this is file name');
      console.log(this.FileList2[i].name);

      if (this.FileList2[i].name == name) {
        this.DaoVanService.getSetting(i);
        break;
      }
    }
  }
  sort(sort: { key: string; value: string }): void {
    this.sortName = sort.key;
    this.sortValue = sort.value;
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
}
