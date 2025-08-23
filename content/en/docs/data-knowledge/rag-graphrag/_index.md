---
title: "RAG & GraphRAG"
description: "Advanced retrieval-augmented generation powered by Supabase Vector with hybrid search, real-time updates, and graph-based reasoning"
weight: 30
---

# RAG & GraphRAG with Supabase

The RAG (Retrieval-Augmented Generation) and GraphRAG components leverage **Supabase Vector** to provide sophisticated information retrieval and reasoning capabilities. With pgvector's native PostgreSQL integration, real-time subscriptions, and ACID guarantees, Supabase enables enterprise-grade RAG systems with unmatched reliability and performance.

## Architecture Overview

```mermaid
graph TB
    A[User Query] --> B[Query Analysis]
    B --> C[Supabase Retrieval Router]
    C --> D[Multi-Modal Retrieval]
    
    subgraph "Supabase Vector Platform"
        D --> E[pgvector Semantic Search]
        D --> F[PostgreSQL Full-text Search]
        D --> G[Graph Traversal (SQL)]
        D --> H[Hybrid Search Functions]
    end
    
    subgraph "Unified Data Layer"
        E --> I[Vector Embeddings]
        F --> J[TSVECTOR Indexes]
        G --> K[Graph Tables]
        H --> L[JSONB Documents]
    end
    
    I --> M[Real-time Context Assembly]
    J --> M
    K --> M
    L --> M
    
    M --> N[Context Optimization]
    N --> O[LLM Generation]
    O --> P[Response Validation]
    P --> Q[Final Response]
    
    subgraph "Supabase Real-time"
        Q --> R[Live Feedback]
        R --> S[Adaptive Learning]
        S --> C
        
        I -.->|Real-time Updates| T[Supabase Subscriptions]
        T -.-> C
    end
```

## Advanced Retrieval Strategies

### Hybrid Search Implementation

```python
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import asyncio
from sklearn.metrics.pairwise import cosine_similarity
import re

@dataclass
class SearchResult:
    content: str
    score: float
    source: str
    metadata: Dict[str, Any]
    retrieval_method: str

class HybridSearchEngine:
    def __init__(self, vector_store, text_search_engine, graph_db):
        self.vector_store = vector_store
        self.text_search_engine = text_search_engine
        self.graph_db = graph_db
        self.query_analyzer = QueryAnalyzer()
        self.result_ranker = ResultRanker()
        
    async def search(self, query: str, top_k: int = 10, 
                    search_strategies: Optional[List[str]] = None) -> List[SearchResult]:
        """Execute hybrid search with multiple strategies"""
        
        # Analyze query to determine optimal search strategies
        query_analysis = await self.query_analyzer.analyze(query)
        
        if search_strategies is None:
            search_strategies = self._select_strategies(query_analysis)
        
        # Execute searches in parallel
        search_tasks = []
        
        if 'semantic' in search_strategies:
            search_tasks.append(self._semantic_search(query, top_k))
            
        if 'keyword' in search_strategies:
            search_tasks.append(self._keyword_search(query, top_k))
            
        if 'graph' in search_strategies:
            search_tasks.append(self._graph_search(query, top_k))
            
        if 'phrase' in search_strategies:
            search_tasks.append(self._phrase_search(query, top_k))
            
        # Collect results
        search_results = await asyncio.gather(*search_tasks)
        
        # Combine and rank results
        all_results = []
        for results in search_results:
            all_results.extend(results)
            
        # Remove duplicates and re-rank
        unique_results = self._deduplicate_results(all_results)
        ranked_results = await self.result_ranker.rank(
            query, unique_results, query_analysis
        )
        
        return ranked_results[:top_k]
        
    async def _semantic_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Perform vector-based semantic search"""
        query_embedding = await self.vector_store.embed_query(query)
        
        # Search with multiple embedding strategies
        results = []
        
        # Standard semantic search
        semantic_results = await self.vector_store.similarity_search(
            query_embedding, top_k=top_k
        )
        
        for result in semantic_results:
            results.append(SearchResult(
                content=result['content'],
                score=result['score'],
                source=result['source'],
                metadata=result['metadata'],
                retrieval_method='semantic'
            ))
            
        # Add hypothetical document embeddings (HyDE)
        hypothetical_doc = await self._generate_hypothetical_document(query)
        if hypothetical_doc:
            hyde_embedding = await self.vector_store.embed_query(hypothetical_doc)
            hyde_results = await self.vector_store.similarity_search(
                hyde_embedding, top_k=top_k//2
            )
            
            for result in hyde_results:
                results.append(SearchResult(
                    content=result['content'],
                    score=result['score'] * 0.9,  # Slightly lower weight
                    source=result['source'],
                    metadata=result['metadata'],
                    retrieval_method='hyde'
                ))
                
        return results
        
    async def _keyword_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Perform keyword-based search with query expansion"""
        # Extract key terms
        key_terms = await self.query_analyzer.extract_key_terms(query)
        
        # Query expansion using synonyms and related terms
        expanded_terms = await self._expand_query_terms(key_terms)
        
        # Construct search query with boosting
        search_query = self._build_boosted_query(key_terms, expanded_terms)
        
        results = await self.text_search_engine.search(
            search_query, top_k=top_k
        )
        
        return [SearchResult(
            content=result['content'],
            score=result['score'],
            source=result['source'],
            metadata=result['metadata'],
            retrieval_method='keyword'
        ) for result in results]
        
    async def _graph_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Perform graph-based search for entity relationships"""
        # Extract entities from query
        entities = await self.query_analyzer.extract_entities(query)
        
        results = []
        
        for entity in entities:
            # Find connected entities and relationships
            graph_results = await self.graph_db.traverse(
                start_entity=entity,
                max_depth=2,
                relationship_types=['RELATED_TO', 'PART_OF', 'INFLUENCES']
            )
            
            for result in graph_results:
                # Generate context from graph structure
                context = self._generate_graph_context(result)
                
                results.append(SearchResult(
                    content=context,
                    score=result['relevance_score'],
                    source=f"graph:{result['path']}",
                    metadata={
                        'entities': result['entities'],
                        'relationships': result['relationships']
                    },
                    retrieval_method='graph'
                ))
                
        return sorted(results, key=lambda x: x.score, reverse=True)[:top_k]

class QueryAnalyzer:
    def __init__(self):
        self.entity_extractor = EntityExtractor()
        self.intent_classifier = IntentClassifier()
        
    async def analyze(self, query: str) -> Dict[str, Any]:
        """Comprehensive query analysis"""
        analysis = {
            'query': query,
            'query_type': await self._classify_query_type(query),
            'entities': await self.entity_extractor.extract(query),
            'intent': await self.intent_classifier.classify(query),
            'complexity_score': self._calculate_complexity(query),
            'key_terms': await self.extract_key_terms(query),
            'semantic_focus': await self._identify_semantic_focus(query)
        }
        
        return analysis
        
    async def _classify_query_type(self, query: str) -> str:
        """Classify query type for strategy selection"""
        patterns = {
            'factual': [r'what is', r'define', r'explain'],
            'comparative': [r'compare', r'difference between', r'versus'],
            'procedural': [r'how to', r'steps to', r'process for'],
            'analytical': [r'why', r'analyze', r'impact of'],
            'temporal': [r'when', r'timeline', r'history of']
        }
        
        query_lower = query.lower()
        
        for query_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, query_lower):
                    return query_type
                    
        return 'general'
        
    def _calculate_complexity(self, query: str) -> float:
        """Calculate query complexity score"""
        factors = {
            'length': len(query.split()) / 20.0,  # Normalize by typical query length
            'entities': len(re.findall(r'\b[A-Z][a-z]+\b', query)) / 5.0,
            'conjunctions': len(re.findall(r'\b(and|or|but|because)\b', query.lower())) / 3.0,
            'questions': len(re.findall(r'\?', query)),
            'technical_terms': len(re.findall(r'\b[A-Z]{2,}\b', query)) / 3.0
        }
        
        complexity = sum(factors.values()) / len(factors)
        return min(1.0, complexity)
```

### Context Window Optimization

```python
import tiktoken
from typing import List, Tuple
import numpy as np

class ContextOptimizer:
    def __init__(self, model_name: str = "gpt-4", max_tokens: int = 8192):
        self.tokenizer = tiktoken.encoding_for_model(model_name)
        self.max_tokens = max_tokens
        self.context_buffer = int(max_tokens * 0.1)  # 10% buffer
        
    def optimize_context(self, query: str, search_results: List[SearchResult],
                        system_prompt: str = "") -> Tuple[str, List[SearchResult]]:
        """Optimize context within token limits"""
        
        # Calculate token budget
        query_tokens = len(self.tokenizer.encode(query))
        system_tokens = len(self.tokenizer.encode(system_prompt))
        available_tokens = self.max_tokens - query_tokens - system_tokens - self.context_buffer
        
        # Score and select results
        scored_results = self._score_results_for_context(query, search_results)
        
        # Progressive context building
        selected_results = []
        current_tokens = 0
        
        for result in scored_results:
            result_tokens = len(self.tokenizer.encode(result.content))
            
            if current_tokens + result_tokens <= available_tokens:
                selected_results.append(result)
                current_tokens += result_tokens
            else:
                # Try to fit truncated version
                truncated_content = self._truncate_content(
                    result.content, 
                    available_tokens - current_tokens
                )
                
                if truncated_content:
                    result.content = truncated_content
                    selected_results.append(result)
                    break
                    
        # Assemble optimized context
        context = self._assemble_context(selected_results)
        
        return context, selected_results
        
    def _score_results_for_context(self, query: str, 
                                 results: List[SearchResult]) -> List[SearchResult]:
        """Score results for context inclusion"""
        query_embedding = self._get_embedding(query)
        
        for result in results:
            # Combine multiple scoring factors
            content_embedding = self._get_embedding(result.content)
            semantic_score = cosine_similarity(
                [query_embedding], [content_embedding]
            )[0][0]
            
            # Diversity penalty (avoid too similar content)
            diversity_score = self._calculate_diversity_score(result, results)
            
            # Recency bonus
            recency_score = self._calculate_recency_score(result)
            
            # Authority bonus
            authority_score = self._calculate_authority_score(result)
            
            # Combined score
            result.context_score = (
                semantic_score * 0.4 +
                result.score * 0.3 +
                diversity_score * 0.1 +
                recency_score * 0.1 +
                authority_score * 0.1
            )
            
        return sorted(results, key=lambda x: x.context_score, reverse=True)
        
    def _truncate_content(self, content: str, max_tokens: int) -> str:
        """Intelligently truncate content"""
        if max_tokens <= 0:
            return ""
            
        # Try to preserve important sentences
        sentences = content.split('. ')
        
        truncated = ""
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence + ". "))
            
            if current_tokens + sentence_tokens <= max_tokens:
                truncated += sentence + ". "
                current_tokens += sentence_tokens
            else:
                # Add partial sentence if there's room
                remaining_tokens = max_tokens - current_tokens - 10
                if remaining_tokens > 20:
                    partial = sentence[:remaining_tokens * 4]  # Rough char estimate
                    truncated += partial + "..."
                break
                
        return truncated.strip()
        
    def _assemble_context(self, results: List[SearchResult]) -> str:
        """Assemble context with proper formatting"""
        context_parts = []
        
        for i, result in enumerate(results):
            context_part = f"[Source {i+1}: {result.source}]\n"
            context_part += f"{result.content}\n"
            
            if result.metadata:
                relevant_metadata = {
                    k: v for k, v in result.metadata.items() 
                    if k in ['author', 'date', 'type', 'confidence']
                }
                if relevant_metadata:
                    context_part += f"Metadata: {relevant_metadata}\n"
                    
            context_parts.append(context_part)
            
        return "\n".join(context_parts)
```

### Multi-hop Reasoning

```python
class GraphRAGEngine:
    def __init__(self, knowledge_graph, llm_client):
        self.kg = knowledge_graph
        self.llm = llm_client
        self.reasoning_chain = []
        
    async def multi_hop_reasoning(self, query: str, max_hops: int = 3) -> Dict[str, Any]:
        """Perform multi-hop reasoning across knowledge graph"""
        
        # Initialize reasoning state
        reasoning_state = {
            'original_query': query,
            'current_entities': [],
            'reasoning_path': [],
            'evidence': [],
            'confidence_scores': []
        }
        
        # Extract initial entities from query
        initial_entities = await self._extract_entities(query)
        reasoning_state['current_entities'] = initial_entities
        
        # Multi-hop traversal
        for hop in range(max_hops):
            hop_results = await self._execute_reasoning_hop(
                reasoning_state, hop
            )
            
            if not hop_results['continue_reasoning']:
                break
                
            reasoning_state = hop_results['updated_state']
            
        # Synthesize final answer
        final_answer = await self._synthesize_answer(reasoning_state)
        
        return {
            'answer': final_answer,
            'reasoning_path': reasoning_state['reasoning_path'],
            'evidence': reasoning_state['evidence'],
            'confidence': np.mean(reasoning_state['confidence_scores']) if reasoning_state['confidence_scores'] else 0.0
        }
        
    async def _execute_reasoning_hop(self, state: Dict, hop_number: int) -> Dict:
        """Execute single reasoning hop"""
        current_entities = state['current_entities']
        
        # Generate reasoning questions for current hop
        reasoning_questions = await self._generate_hop_questions(
            state['original_query'], 
            state['reasoning_path'],
            current_entities,
            hop_number
        )
        
        hop_evidence = []
        new_entities = set()
        
        for question in reasoning_questions:
            # Query knowledge graph
            graph_results = await self.kg.query_with_reasoning(
                entities=current_entities,
                question=question,
                max_depth=2
            )
            
            # Process results
            for result in graph_results:
                evidence_piece = {
                    'question': question,
                    'fact': result['fact'],
                    'entities': result['entities'],
                    'relationships': result['relationships'],
                    'confidence': result['confidence'],
                    'hop': hop_number
                }
                
                hop_evidence.append(evidence_piece)
                new_entities.update(result['entities'])
                
        # Update reasoning state
        state['evidence'].extend(hop_evidence)
        state['reasoning_path'].append({
            'hop': hop_number,
            'questions': reasoning_questions,
            'entities_explored': current_entities,
            'new_entities_found': list(new_entities)
        })
        
        # Determine if reasoning should continue
        continue_reasoning = await self._should_continue_reasoning(
            state, new_entities, hop_number
        )
        
        if continue_reasoning:
            state['current_entities'] = list(new_entities)
            
        return {
            'updated_state': state,
            'continue_reasoning': continue_reasoning
        }
        
    async def _generate_hop_questions(self, original_query: str,
                                    reasoning_path: List[Dict],
                                    current_entities: List[str],
                                    hop_number: int) -> List[str]:
        """Generate questions for current reasoning hop"""
        
        context = f"""
        Original query: {original_query}
        Current reasoning hop: {hop_number + 1}
        Current entities: {current_entities}
        Previous reasoning: {reasoning_path}
        
        Generate 2-3 specific questions that would help answer the original query
        by exploring relationships and properties of the current entities.
        Focus on finding connections that lead toward the answer.
        """
        
        response = await self.llm.generate(
            prompt=context,
            max_tokens=200,
            temperature=0.3
        )
        
        # Extract questions from response
        questions = self._extract_questions_from_text(response)
        return questions[:3]  # Limit to 3 questions per hop
        
    async def _synthesize_answer(self, reasoning_state: Dict) -> str:
        """Synthesize final answer from reasoning evidence"""
        
        synthesis_prompt = f"""
        Original Question: {reasoning_state['original_query']}
        
        Reasoning Path: {reasoning_state['reasoning_path']}
        
        Evidence Collected:
        """
        
        for evidence in reasoning_state['evidence']:
            synthesis_prompt += f"- {evidence['fact']} (Confidence: {evidence['confidence']:.2f})\n"
            
        synthesis_prompt += """
        
        Based on this multi-hop reasoning through the knowledge graph,
        provide a comprehensive answer to the original question.
        Include confidence indicators and cite the evidence used.
        """
        
        answer = await self.llm.generate(
            prompt=synthesis_prompt,
            max_tokens=500,
            temperature=0.2
        )
        
        return answer
```

### Adaptive RAG

```python
import mlflow
from sklearn.metrics import accuracy_score, f1_score
import numpy as np
from typing import Dict, List, Tuple

class AdaptiveRAGSystem:
    def __init__(self, base_retrieval_system):
        self.base_system = base_retrieval_system
        self.performance_tracker = PerformanceTracker()
        self.strategy_optimizer = StrategyOptimizer()
        self.feedback_collector = FeedbackCollector()
        
    async def adaptive_retrieve(self, query: str, 
                              context: Dict[str, Any]) -> List[SearchResult]:
        """Adaptively select and execute retrieval strategy"""
        
        # Analyze query and context
        query_features = await self._extract_query_features(query, context)
        
        # Select optimal strategy based on learned patterns
        strategy_config = await self.strategy_optimizer.select_strategy(
            query_features
        )
        
        # Execute retrieval with selected strategy
        with self.performance_tracker.track_retrieval(query, strategy_config):
            results = await self.base_system.search(
                query=query,
                top_k=strategy_config['top_k'],
                search_strategies=strategy_config['strategies'],
                retrieval_params=strategy_config['params']
            )
            
        # Post-process results based on learned preferences
        optimized_results = await self._post_process_results(
            results, query_features, strategy_config
        )
        
        return optimized_results
        
    async def learn_from_feedback(self, query: str, results: List[SearchResult],
                                user_feedback: Dict[str, Any]):
        """Learn from user feedback to improve future retrievals"""
        
        # Collect feedback
        feedback_record = {
            'query': query,
            'results': results,
            'user_feedback': user_feedback,
            'timestamp': datetime.utcnow().isoformat(),
            'query_features': await self._extract_query_features(query, {})
        }
        
        await self.feedback_collector.store_feedback(feedback_record)
        
        # Update strategy optimization models
        if len(await self.feedback_collector.get_recent_feedback(100)) >= 100:
            await self.strategy_optimizer.retrain()
            
    async def _extract_query_features(self, query: str, 
                                    context: Dict[str, Any]) -> Dict[str, float]:
        """Extract features for strategy selection"""
        features = {
            'query_length': len(query.split()),
            'has_entities': len(await self._extract_entities(query)) > 0,
            'complexity_score': self._calculate_complexity(query),
            'domain_specificity': await self._calculate_domain_specificity(query),
            'temporal_aspect': self._has_temporal_aspect(query),
            'user_expertise': context.get('user_expertise_level', 0.5),
            'task_type': self._classify_task_type(query),
            'urgency': context.get('urgency_level', 0.5)
        }
        
        return features
        
class StrategyOptimizer:
    def __init__(self):
        self.model = None
        self.strategy_performance = {}
        self.mlflow_client = mlflow.tracking.MlflowClient()
        
    async def select_strategy(self, query_features: Dict[str, float]) -> Dict[str, Any]:
        """Select optimal retrieval strategy based on query features"""
        
        if self.model is None:
            # Use default strategy
            return self._get_default_strategy()
            
        # Predict optimal strategy
        feature_vector = np.array(list(query_features.values())).reshape(1, -1)
        strategy_scores = self.model.predict_proba(feature_vector)[0]
        
        # Select strategy with highest predicted success
        best_strategy_idx = np.argmax(strategy_scores)
        
        strategy_configs = [
            {  # Strategy 0: Semantic-focused
                'strategies': ['semantic', 'hyde'],
                'top_k': 15,
                'params': {'semantic_weight': 0.8, 'keyword_weight': 0.2}
            },
            {  # Strategy 1: Keyword-focused
                'strategies': ['keyword', 'phrase'],
                'top_k': 20,
                'params': {'semantic_weight': 0.3, 'keyword_weight': 0.7}
            },
            {  # Strategy 2: Graph-focused
                'strategies': ['graph', 'semantic'],
                'top_k': 12,
                'params': {'max_hops': 2, 'semantic_weight': 0.6}
            },
            {  # Strategy 3: Hybrid balanced
                'strategies': ['semantic', 'keyword', 'graph'],
                'top_k': 18,
                'params': {'semantic_weight': 0.5, 'keyword_weight': 0.3, 'graph_weight': 0.2}
            }
        ]
        
        return strategy_configs[best_strategy_idx]
        
    async def retrain(self):
        """Retrain strategy selection model"""
        # Load training data from feedback
        training_data = await self._prepare_training_data()
        
        if len(training_data) < 50:
            return  # Need more data
            
        # Start MLflow run
        with mlflow.start_run():
            # Train model
            from sklearn.ensemble import RandomForestClassifier
            
            X, y = training_data['features'], training_data['labels']
            
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            model.fit(X, y)
            
            # Evaluate model
            y_pred = model.predict(X)
            accuracy = accuracy_score(y, y_pred)
            f1 = f1_score(y, y_pred, average='weighted')
            
            # Log metrics
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("f1_score", f1)
            
            # Log model
            mlflow.sklearn.log_model(model, "strategy_optimizer")
            
            # Update current model
            self.model = model
            
            return {
                'accuracy': accuracy,
                'f1_score': f1,
                'training_samples': len(training_data)
            }
```

### Cross-lingual Retrieval

```python
from transformers import MarianMTModel, MarianTokenizer
import torch

class CrossLingualRAG:
    def __init__(self, supported_languages: List[str]):
        self.supported_languages = supported_languages
        self.translation_models = {}
        self.multilingual_embedder = MultilingualEmbedder()
        self.language_detector = LanguageDetector()
        
        # Load translation models
        self._load_translation_models()
        
    def _load_translation_models(self):
        """Load translation models for supported languages"""
        for lang in self.supported_languages:
            if lang != 'en':  # Assuming English as pivot language
                # To English
                model_name = f"Helsinki-NLP/opus-mt-{lang}-en"
                self.translation_models[f"{lang}-en"] = {
                    'model': MarianMTModel.from_pretrained(model_name),
                    'tokenizer': MarianTokenizer.from_pretrained(model_name)
                }
                
                # From English
                model_name = f"Helsinki-NLP/opus-mt-en-{lang}"
                self.translation_models[f"en-{lang}"] = {
                    'model': MarianMTModel.from_pretrained(model_name),
                    'tokenizer': MarianTokenizer.from_pretrained(model_name)
                }
                
    async def cross_lingual_search(self, query: str, 
                                 target_languages: List[str] = None) -> List[SearchResult]:
        """Perform cross-lingual retrieval"""
        
        # Detect query language
        query_lang = await self.language_detector.detect(query)
        
        if target_languages is None:
            target_languages = self.supported_languages
            
        # Translate query to all target languages
        translated_queries = {}
        
        if query_lang != 'en':
            # Translate to English first
            english_query = await self._translate(query, query_lang, 'en')
            translated_queries['en'] = english_query
        else:
            translated_queries['en'] = query
            
        # Translate to other target languages
        for lang in target_languages:
            if lang != query_lang and lang != 'en':
                if query_lang == 'en':
                    translated_queries[lang] = await self._translate(query, 'en', lang)
                else:
                    # Use English as pivot
                    translated_queries[lang] = await self._translate(
                        translated_queries['en'], 'en', lang
                    )
                    
        # Perform retrieval in multiple languages
        all_results = []
        
        for lang, translated_query in translated_queries.items():
            # Search in language-specific collections
            lang_results = await self._search_in_language(
                translated_query, lang
            )
            
            # Translate results back to query language if needed
            if lang != query_lang:
                lang_results = await self._translate_results(
                    lang_results, lang, query_lang
                )
                
            all_results.extend(lang_results)
            
        # Merge and rank cross-lingual results
        merged_results = await self._merge_cross_lingual_results(
            all_results, query, query_lang
        )
        
        return merged_results
        
    async def _translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text between languages"""
        model_key = f"{source_lang}-{target_lang}"
        
        if model_key not in self.translation_models:
            # Use English as pivot
            if source_lang != 'en':
                english_text = await self._translate(text, source_lang, 'en')
                return await self._translate(english_text, 'en', target_lang)
            else:
                raise ValueError(f"Translation model not found: {model_key}")
                
        model_info = self.translation_models[model_key]
        model = model_info['model']
        tokenizer = model_info['tokenizer']
        
        # Tokenize
        inputs = tokenizer.encode(text, return_tensors="pt", truncation=True)
        
        # Generate translation
        with torch.no_grad():
            outputs = model.generate(inputs, max_length=512, num_beams=4)
            
        # Decode
        translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return translated
```

### Multimodal RAG

```python
from PIL import Image
import torch
from transformers import CLIPModel, CLIPProcessor

class MultimodalRAG:
    def __init__(self, vector_store, image_processor):
        self.vector_store = vector_store
        self.image_processor = image_processor
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
    async def multimodal_search(self, query: str, 
                              query_image: Optional[Image.Image] = None,
                              modalities: List[str] = None) -> List[SearchResult]:
        """Search across multiple modalities"""
        
        if modalities is None:
            modalities = ['text', 'image', 'video', 'audio']
            
        search_tasks = []
        
        # Text search
        if 'text' in modalities:
            search_tasks.append(self._text_search(query))
            
        # Image search
        if 'image' in modalities:
            if query_image is not None:
                search_tasks.append(self._image_search(query_image, query))
            else:
                # Generate image from text query
                image_query_embedding = await self._text_to_image_embedding(query)
                search_tasks.append(self._image_embedding_search(image_query_embedding))
                
        # Video search
        if 'video' in modalities:
            search_tasks.append(self._video_search(query, query_image))
            
        # Audio search (if query contains audio-related terms)
        if 'audio' in modalities and self._is_audio_query(query):
            search_tasks.append(self._audio_search(query))
            
        # Execute all searches
        search_results = await asyncio.gather(*search_tasks)
        
        # Combine and rank multimodal results
        all_results = []
        for results in search_results:
            all_results.extend(results)
            
        # Apply cross-modal relevance scoring
        ranked_results = await self._rank_multimodal_results(
            query, query_image, all_results
        )
        
        return ranked_results
        
    async def _text_to_image_embedding(self, text: str) -> np.ndarray:
        """Convert text query to image embedding space"""
        inputs = self.clip_processor(text=[text], return_tensors="pt", padding=True)
        
        with torch.no_grad():
            text_features = self.clip_model.get_text_features(**inputs)
            
        return text_features.numpy()[0]
        
    async def _image_search(self, query_image: Image.Image, 
                          text_query: str = "") -> List[SearchResult]:
        """Search for similar images"""
        # Extract image features
        inputs = self.clip_processor(images=query_image, return_tensors="pt")
        
        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)
            
        image_embedding = image_features.numpy()[0]
        
        # Search image vector store
        results = await self.vector_store.similarity_search(
            embedding=image_embedding,
            collection='images',
            top_k=20
        )
        
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                content=result['description'],
                score=result['score'],
                source=result['image_path'],
                metadata={
                    'modality': 'image',
                    'image_path': result['image_path'],
                    'image_features': result.get('features', {}),
                    'extracted_text': result.get('ocr_text', '')
                },
                retrieval_method='multimodal_image'
            ))
            
        return search_results
        
    async def _video_search(self, query: str, 
                          query_image: Optional[Image.Image] = None) -> List[SearchResult]:
        """Search video content using multiple strategies"""
        search_strategies = []
        
        # Text-based video search (transcripts, metadata)
        search_strategies.append(
            self.vector_store.similarity_search(
                query=query,
                collection='video_transcripts',
                top_k=15
            )
        )
        
        # Visual similarity search if image provided
        if query_image is not None:
            # Extract keyframes and compare
            image_embedding = await self._extract_image_embedding(query_image)
            search_strategies.append(
                self.vector_store.similarity_search(
                    embedding=image_embedding,
                    collection='video_keyframes',
                    top_k=10
                )
            )
            
        # Audio similarity search for videos with speech
        audio_query_embedding = await self._text_to_audio_embedding(query)
        search_strategies.append(
            self.vector_store.similarity_search(
                embedding=audio_query_embedding,
                collection='video_audio',
                top_k=10
            )
        )
        
        # Combine video search results
        all_video_results = await asyncio.gather(*search_strategies)
        
        # Merge and deduplicate by video ID
        video_results_map = {}
        
        for strategy_results in all_video_results:
            for result in strategy_results:
                video_id = result['video_id']
                
                if video_id not in video_results_map:
                    video_results_map[video_id] = SearchResult(
                        content=result['transcript_excerpt'],
                        score=result['score'],
                        source=result['video_path'],
                        metadata={
                            'modality': 'video',
                            'video_id': video_id,
                            'timestamp': result.get('timestamp', 0),
                            'keyframe_matches': [],
                            'audio_matches': []
                        },
                        retrieval_method='multimodal_video'
                    )
                else:
                    # Boost score for multiple matches
                    video_results_map[video_id].score += result['score'] * 0.3
                    
                # Add specific match information
                if 'keyframe' in result:
                    video_results_map[video_id].metadata['keyframe_matches'].append({
                        'timestamp': result['timestamp'],
                        'similarity': result['score']
                    })
                    
        return list(video_results_map.values())
```

## Performance Optimization

### Caching & Memoization

```python
import hashlib
import pickle
from functools import wraps
import redis
from typing import Optional, Callable, Any

class RAGCacheManager:
    def __init__(self, redis_client: redis.Redis, 
                 default_ttl: int = 3600):
        self.redis = redis_client
        self.default_ttl = default_ttl
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'invalidations': 0
        }
        
    def cached_retrieval(self, ttl: Optional[int] = None):
        """Decorator for caching retrieval results"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)
                
                # Try to get from cache
                cached_result = self._get_cached_result(cache_key)
                if cached_result is not None:
                    self.cache_stats['hits'] += 1
                    return cached_result
                    
                # Execute function
                result = await func(*args, **kwargs)
                
                # Cache result
                self._cache_result(cache_key, result, ttl or self.default_ttl)
                self.cache_stats['misses'] += 1
                
                return result
                
            return wrapper
        return decorator
        
    def _generate_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate deterministic cache key"""
        # Create hashable representation
        key_data = {
            'function': func_name,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        
        # Hash the key data
        key_string = pickle.dumps(key_data, protocol=pickle.HIGHEST_PROTOCOL)
        key_hash = hashlib.sha256(key_string).hexdigest()
        
        return f"rag_cache:{func_name}:{key_hash}"
        
    def _get_cached_result(self, cache_key: str) -> Optional[Any]:
        """Retrieve cached result"""
        try:
            cached_data = self.redis.get(cache_key)
            if cached_data:
                return pickle.loads(cached_data)
        except Exception as e:
            # Log error but don't fail
            print(f"Cache retrieval error: {e}")
            
        return None
        
    def _cache_result(self, cache_key: str, result: Any, ttl: int):
        """Cache result with TTL"""
        try:
            serialized_result = pickle.dumps(result, protocol=pickle.HIGHEST_PROTOCOL)
            self.redis.setex(cache_key, ttl, serialized_result)
        except Exception as e:
            # Log error but don't fail
            print(f"Cache storage error: {e}")
            
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        try:
            keys = list(self.redis.scan_iter(match=f"rag_cache:*{pattern}*"))
            if keys:
                self.redis.delete(*keys)
                self.cache_stats['invalidations'] += len(keys)
        except Exception as e:
            print(f"Cache invalidation error: {e}")
```

### Query Optimization

```python
class QueryOptimizer:
    def __init__(self):
        self.query_patterns = {}
        self.optimization_rules = [
            self._optimize_entity_queries,
            self._optimize_temporal_queries,
            self._optimize_complex_queries,
            self._optimize_similarity_thresholds
        ]
        
    async def optimize_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply optimization rules to query"""
        
        optimized_config = {
            'original_query': query,
            'optimized_query': query,
            'search_params': {
                'top_k': 10,
                'similarity_threshold': 0.7,
                'max_hops': 2
            },
            'strategy_weights': {
                'semantic': 0.6,
                'keyword': 0.3,
                'graph': 0.1
            }
        }
        
        # Apply optimization rules
        for rule in self.optimization_rules:
            optimized_config = await rule(optimized_config, context)
            
        return optimized_config
        
    async def _optimize_entity_queries(self, config: Dict, context: Dict) -> Dict:
        """Optimize queries with many entities"""
        query = config['optimized_query']
        entities = await self._extract_entities(query)
        
        if len(entities) > 3:
            # Boost graph search for entity-heavy queries
            config['strategy_weights']['graph'] = 0.4
            config['strategy_weights']['semantic'] = 0.4
            config['strategy_weights']['keyword'] = 0.2
            
            # Increase max hops for exploration
            config['search_params']['max_hops'] = 3
            
            # Lower similarity threshold to catch more connections
            config['search_params']['similarity_threshold'] = 0.6
            
        return config
        
    async def _optimize_temporal_queries(self, config: Dict, context: Dict) -> Dict:
        """Optimize time-sensitive queries"""
        query = config['optimized_query']
        
        temporal_indicators = ['recent', 'latest', 'current', 'today', 'yesterday', 'last']
        
        if any(indicator in query.lower() for indicator in temporal_indicators):
            # Add recency boost to search parameters
            config['search_params']['recency_boost'] = True
            config['search_params']['time_decay_factor'] = 0.1
            
            # Increase top_k to get more recent results
            config['search_params']['top_k'] = 15
            
        return config
        
    async def _optimize_similarity_thresholds(self, config: Dict, context: Dict) -> Dict:
        """Dynamically adjust similarity thresholds"""
        query_complexity = context.get('query_complexity', 0.5)
        user_expertise = context.get('user_expertise', 0.5)
        
        # Adjust threshold based on complexity and expertise
        base_threshold = config['search_params']['similarity_threshold']
        
        # Complex queries may need lower threshold for broader search
        complexity_adjustment = -0.1 * query_complexity
        
        # Expert users may want more precise results
        expertise_adjustment = 0.1 * user_expertise
        
        new_threshold = base_threshold + complexity_adjustment + expertise_adjustment
        new_threshold = max(0.4, min(0.9, new_threshold))  # Clamp to reasonable range
        
        config['search_params']['similarity_threshold'] = new_threshold
        
        return config
```

## Monitoring & Analytics

```python
import structlog
from prometheus_client import Counter, Histogram, Gauge
from datetime import datetime, timedelta

class RAGAnalytics:
    def __init__(self):
        # Prometheus metrics
        self.query_count = Counter(
            'rag_queries_total',
            'Total RAG queries',
            ['query_type', 'strategy', 'status']
        )
        
        self.retrieval_latency = Histogram(
            'rag_retrieval_duration_seconds',
            'RAG retrieval duration',
            ['strategy', 'complexity_level']
        )
        
        self.context_utilization = Gauge(
            'rag_context_utilization_ratio',
            'Context utilization ratio',
            ['strategy']
        )
        
        self.answer_quality_score = Histogram(
            'rag_answer_quality_score',
            'RAG answer quality score',
            ['strategy', 'query_type']
        )
        
        # Structured logging
        self.logger = structlog.get_logger()
        
    async def track_query_execution(self, query: str, strategy: str,
                                  execution_time: float, results: List[SearchResult],
                                  quality_score: Optional[float] = None):
        """Track query execution metrics"""
        
        # Classify query
        query_type = await self._classify_query(query)
        complexity_level = self._calculate_complexity_level(query)
        
        # Update metrics
        self.query_count.labels(
            query_type=query_type,
            strategy=strategy,
            status='success'
        ).inc()
        
        self.retrieval_latency.labels(
            strategy=strategy,
            complexity_level=complexity_level
        ).observe(execution_time)
        
        if quality_score is not None:
            self.answer_quality_score.labels(
                strategy=strategy,
                query_type=query_type
            ).observe(quality_score)
            
        # Log detailed information
        self.logger.info(
            "rag_query_executed",
            query=query,
            query_type=query_type,
            strategy=strategy,
            execution_time=execution_time,
            result_count=len(results),
            quality_score=quality_score,
            complexity_level=complexity_level
        )
        
    async def analyze_retrieval_effectiveness(self, 
                                           time_window_hours: int = 24) -> Dict[str, Any]:
        """Analyze retrieval effectiveness over time window"""
        
        # This would typically query your metrics backend
        # Showing conceptual analysis structure
        
        analysis = {
            'time_window': f"{time_window_hours}h",
            'total_queries': await self._count_queries(time_window_hours),
            'average_latency': await self._average_latency(time_window_hours),
            'strategy_performance': await self._strategy_performance(time_window_hours),
            'quality_trends': await self._quality_trends(time_window_hours),
            'optimization_recommendations': []
        }
        
        # Generate recommendations
        if analysis['average_latency'] > 2.0:  # seconds
            analysis['optimization_recommendations'].append({
                'type': 'performance',
                'message': 'Consider adding caching or reducing top_k values',
                'priority': 'high'
            })
            
        if analysis['strategy_performance'].get('semantic', {}).get('success_rate', 0) < 0.7:
            analysis['optimization_recommendations'].append({
                'type': 'accuracy',
                'message': 'Semantic search performance is low, consider retraining embeddings',
                'priority': 'medium'
            })
            
        return analysis
        
    def generate_insights_report(self, period_days: int = 7) -> str:
        """Generate comprehensive insights report"""
        
        report = f"""
        # RAG System Performance Report
        ## Period: Last {period_days} days
        
        ### Key Metrics
        - Total Queries: {self._get_metric_value('rag_queries_total', period_days)}
        - Average Latency: {self._get_metric_value('rag_retrieval_duration_seconds', period_days):.2f}s
        - Success Rate: {self._calculate_success_rate(period_days):.1%}
        
        ### Strategy Performance
        """
        
        strategies = ['semantic', 'keyword', 'graph', 'hybrid']
        for strategy in strategies:
            perf = self._get_strategy_performance(strategy, period_days)
            report += f"""
        #### {strategy.title()} Strategy
        - Queries: {perf['count']}
        - Avg Latency: {perf['latency']:.2f}s
        - Quality Score: {perf['quality']:.2f}
        """
        
        report += """
        ### Recommendations
        """
        
        recommendations = self._generate_recommendations(period_days)
        for rec in recommendations:
            report += f"- {rec}\n"
            
        return report
```

## Next Steps

- **[Knowledge Management](../knowledge-management/)** - Set up automated knowledge extraction and curation
- **[ML/AI Integration](../ml-ai-integration/)** - Connect with machine learning workflows  
- **[Performance Optimization](../performance-optimization/)** - Advanced optimization techniques
- **[Security & Privacy](../security-privacy/)** - Implement security best practices

The RAG & GraphRAG component provides the intelligence layer that transforms static knowledge into dynamic, contextual responses, enabling your AI systems to provide accurate, relevant, and up-to-date information to users.