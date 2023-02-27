//
//  ContentView.swift
//  PillDispenser
//
//  Created by Ben Randoing on 2/12/23.
//

import Combine
import SwiftUI

class Order: ObservableObject {
    
    var didChange = PassthroughSubject<Void, Never>()
    
    static let types = ["Tylenol", "Advil", "Aleve", "Ibuprofen"]
    
    @Published var type = 0 { didSet { update() } }
    @Published var quantity = 1 { didSet { update() } }
    
    @Published var name = "" { didSet { update() } }
    
    var isValid: Bool {
        if name.isEmpty {
            return false
        }
        return true
    }
    
    func update() {
        print("update called")
        didChange.send(())
    }
}


struct ContentView: View {
    @ObservedObject var order = Order()
    var body: some View {
        NavigationView {
            Form {
                Section{
                    Picker(selection: $order.type, label: Text("Select Medication")) {
                        ForEach(0 ..< Order.types.count) {
                            Text(Order.types[$0]).tag($0)
                        }
                    }
                    .pickerStyle(.wheel)
                    
                    Stepper(value: $order.quantity, in: 1...20) {
                        Text("Number of Pills: \(order.quantity)")
                    }
                }
                
                Section{
                    TextField("Name", text: $order.name)
                }
                
                Section{
                    Button(action: {
                        // place the order
                        self.apiCall()
                        print("hit")
                    }) {
                        Text("Place Order")
                    }
                }.disabled(!order.isValid)
            }
            .navigationBarTitle("Pill Dispenser")
        }
    }
    
    func apiCall() {
        print("ran")
        guard let url = URL(string: "http://127.0.0.1:5000") else {
            return
        }
        
        var request = URLRequest(url: url)
        
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let body: [String: AnyHashable] = [
            "name": "test"
        ]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: .fragmentsAllowed)
        
        print("here")
        let task = URLSession.shared.dataTask(with: request) { data, _, error in
            guard let data = data, error == nil else{
                return
            }
            do {
                print("in")
                let response = try JSONSerialization.jsonObject(with: data, options: .fragmentsAllowed)
                print("Success")
            }
            catch {
                print("oops")
                print(error)
            }
        }
        task.resume()
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
