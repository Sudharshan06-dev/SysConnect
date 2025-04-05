import { Component } from '@angular/core';
import {ColumnComponent, DataBindingDirective, GridComponent} from '@progress/kendo-angular-grid';
import {CompositeFilterDescriptor} from '@progress/kendo-data-query';


@Component({
  selector: 'app-application-enrollment-details',
  standalone: true,
  imports: [
    GridComponent,
    ColumnComponent,
    DataBindingDirective
  ],
  templateUrl: './applicant-details.component.html',
  styleUrl: './applicant-details.component.css'
})
export class ApplicantDetailsComponent {

  public filter: CompositeFilterDescriptor = {
    logic: "and",
    filters: [],
  };

  public gridData = [
    {
      ReferenceNumber: "85AB671WE",
      FirstName: "Sudharshan",
      LastName: "Madhavan",
      Email: "sudharshan.madhavan1998@outlook.com",
      Username: "Sudharshan06",
      Role: "Student",
      Degree: "Computer Science",
      Major: "Software Engineering",
      Status: "Pending"
    },
    {
      ReferenceNumber: "01NC671AJ",
      FirstName: "Ratika",
      LastName: "Moolchandani",
      Email: "ratika@csu.fullerton.edu",
      Username: "Ratika",
      Role: "Professor",
      Degree: "Computer Science",
      Major: "Software Engineering",
      Status: "Pending"
    }
  ];

  public filterChange(filter: CompositeFilterDescriptor): void {
    this.filter = filter;
  }

}
