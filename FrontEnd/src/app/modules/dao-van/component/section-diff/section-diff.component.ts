import { Component, OnInit } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';

@Component({
  selector: 'app-section-diff',
  templateUrl: './section-diff.component.html',
  styleUrls: ['./section-diff.component.scss'],
})
export class SectionDiffComponent implements OnInit {
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  data = [
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',
    },
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',
    },
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',
    },
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',
    },
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
