targetScope = 'subscription'

param location string = 'westeurope'
param rgName string = 'second_resource_group'

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: rgName
  location: location
}


module keyVaultModule 'keyvault.bicep' = {
  name: 'keyVaultModule'
  scope: rg
  params: {
    location: location
  }
  dependsOn: [
    rg
  ]
}




