import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ListInputFileComponent } from './list-input-file.component';

describe('ListInputFileComponent', () => {
  let component: ListInputFileComponent;
  let fixture: ComponentFixture<ListInputFileComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [ListInputFileComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(ListInputFileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
