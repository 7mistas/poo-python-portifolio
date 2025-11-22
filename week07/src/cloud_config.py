import os
from pathlib import Path
from typing import Dict

class Cloud_Config:
    def __init__(self):
        self.ambiente = os.getenv('AMBIENTE', 'desenvolvimento') #dev ou prod.
        self.config = self.carregar_config()
        
    def carregar_config(self) -> Dict:
        if self.ambiente == 'producao':
            # Produção na nuvem.
            return {
                    'database': {
                    'host': 'chat-db.abc123.us-east-1.rds.amazonaws.com',
                    'port': 5432,
                    'name': 'chat_prod',
                    'tipo': 'postgresql'
                },
                    'storage': {
                    'tipo': 's3',
                    'bucket': 'chat-arquivos',
                    'region': 'us-east-1',
                },
                    'servidor': {
                    'host': '0.0.0.0',
                    'port': 8080,
                    'workers': 'chat_prod',
                }
            }
        else:
            # Desenvolvimento local.
            return {
                'database': {
                    'host': 'localhost',
                    'name': 'chat.db',
                    'tipo': 'sqlite'
                },
                'storage': {
                    'tipo': 'local',
                    'path': str(Path(__file__).parent)
                },
                'servidor': {
                    'host': 'localhost',
                    'port': 8000
                }
            }

    def get_storage_config(self) -> Dict:
        return self.config['storage']

    # Menu da simulação de deploy.
    def simular_deploy_aws(self):
        print("\n" + "=" * 71)
        print(" " * 20 + "🚀 SIMULAÇÃO DE DEPLOY AWS")
        print("=" * 71)
        
        print("\n[1/5] 📦 Empacotando aplicação...")
        print("      ✓ Código compactado")
        print("      ✓ Dependências incluídas")
        
        print("\n[2/5] ☁️  Upload para S3...")
        print(f"      ✓ Bucket: {self.config.get('storage', {}).get('bucket', 'N/A')}")
        print("      ✓ Arquivos enviados")
        
        print("\n[3/5] 🖥️  Deploy no EC2...")
        print("      ✓ Instância t3.micro criada")
        print("      ✓ Python 3.11 instalado")
        print("      ✓ Aplicação iniciada")
        
        print("\n[4/5] 🔒 Configurando segurança...")
        print("      ✓ Security Group configurado")
        print("      ✓ SSL/TLS habilitado")
        print("      ✓ Firewall ativo")
        
        print("\n[5/5] 🌐 Configurando DNS...")
        print("      ✓ Domínio: chat.n/a.com")
        print("      ✓ Load Balancer ativo")
        
        print("\n" + "=" * 71)
        print("✅ Deploy concluído com sucesso!")
        print("🌍 Aplicação disponível em: https://chat.n/a.com")
        print("=" * 71 + "\n")

