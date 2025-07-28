"""
Persona-driven content matching and relevance scoring
"""

import logging
import json
from typing import Dict, List, Tuple
from services.round1b.embedding_generator import EmbeddingGenerator

class PersonaMatcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.embedding_generator = EmbeddingGenerator()
        
        # Persona expansion templates
        self.persona_templates = {
            'software_engineer': [
                'technical implementation',
                'coding practices',
                'system architecture',
                'development tools',
                'programming languages'
            ],
            'product_manager': [
                'product strategy',
                'user requirements',
                'market analysis',
                'roadmap planning',
                'stakeholder management'
            ],
            'data_scientist': [
                'machine learning',
                'statistical analysis',
                'data modeling',
                'research methodology',
                'analytics tools'
            ]
        }
    
    def expand_query(self, job_role: str, query: str) -> str:
        """Expand query with persona-specific context"""
        expanded_terms = []
        
        # Add original query
        expanded_terms.append(query)
        
        # Add role-specific terms
        role_key = job_role.lower().replace(' ', '_')
        if role_key in self.persona_templates:
            relevant_terms = self.persona_templates[role_key]
            expanded_terms.extend(relevant_terms[:3])  # Limit expansion
        
        return ' '.join(expanded_terms)
    
    def calculate_persona_relevance(self, content: str, job_role: str, query: str) -> float:
        """Calculate relevance score for persona-specific content"""
        
        # Generate embeddings
        content_embedding = self.embedding_generator.encode_single(content)
        query_embedding = self.embedding_generator.encode_single(query)
        
        # Expand query with persona context
        expanded_query = self.expand_query(job_role, query)
        persona_embedding = self.embedding_generator.encode_single(expanded_query)
        
        # Calculate similarities
        content_query_sim = self.embedding_generator.calculate_similarity(
            content_embedding, query_embedding
        )
        content_persona_sim = self.embedding_generator.calculate_similarity(
            content_embedding, persona_embedding
        )
        
        # Weighted combination (70% query relevance, 30% persona fit)
        final_score = 0.7 * content_query_sim + 0.3 * content_persona_sim
        
        return float(final_score)
    
    def rank_sections(self, sections: List[Dict], job_role: str, query: str) -> List[Tuple[Dict, float]]:
        """Rank document sections by persona relevance"""
        scored_sections = []
        
        for section in sections:
            # Combine section text and context
            section_text = section.get('text', '')
            if section.get('children'):
                # Include child content for context
                child_texts = [child.get('text', '') for child in section['children']]
                section_text += ' ' + ' '.join(child_texts)
            
            # Calculate relevance score
            score = self.calculate_persona_relevance(section_text, job_role, query)
            scored_sections.append((section, score))
        
        # Sort by score (descending)
        return sorted(scored_sections, key=lambda x: x[1], reverse=True)
